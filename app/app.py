from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse, UserRead, UserCreate, UserUpdate
from app.db import Post, create_db_and_tables, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession     
from contextlib import asynccontextmanager  
from sqlalchemy import select
from app.image import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile
from app.users import auth_backend, current_active_user, fastapi_users, current_active_user_optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    
app = FastAPI(lifespan = lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend),prefix="/auth/jwt",tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead,UserCreate),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead,UserUpdate),prefix="/auth",tags=["auth"])

@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(...),
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file(
            file = open(temp_file_path, "rb"),
            file_name = file.filename,
            options = UploadFileRequestOptions(
                use_unique_file_name = True,
                tags = ["backend-upload"]
            )
        )
        
        if upload_result.response_metadata.http_status_code != 200:
            raise HTTPException(status_code=500, detail="Image upload failed")

        post = Post(
            user_id = user.id,
            caption = caption,
            url = upload_result.url,
            file_type = "video" if file.content_type.startswith("video/") else "image",
            file_name = upload_result.name
        )
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return PostResponse(
            id = post.id,
            user_id = str(post.user_id),
            caption = post.caption,
            url = post.url,
            file_type = post.file_type,
            file_name = post.file_name,
            created_at = post.created_at.isoformat(),
            is_owner = True,
            email = user.email
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()

@app.get("/feed")
async def get_feed(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user_optional)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    users_dict = {u.id: u.email for u in users}

    post_data = []
    for post in posts:
        post_data.append(PostResponse(
            id=post.id,
            user_id=str(post.user_id),
            caption=post.caption,
            url=post.url,
            file_type=post.file_type,
            file_name=post.file_name,
            created_at=post.created_at.isoformat(),
            is_owner=post.user_id == user.id if user else False,
            email=users_dict.get(post.user_id, "Unknown")
        ))
    return {"posts": post_data}

@app.delete("/post/{post_id}")
async def delete_post(
        post_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user_optional)
):
    if not user:
        raise HTTPException(status_code=401, detail="You are not authorized to delete this post")
    try:
        result = await session.execute(select(Post).where(Post.id == post_id))
        post = result.scalars().first()


        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this post")
        await session.delete(post)
        await session.commit()
        return {"success": True, "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))