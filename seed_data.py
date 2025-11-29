import asyncio
from app.db import create_db_and_tables, async_session_maker, Post

async def seed():
    await create_db_and_tables()
    async with async_session_maker() as session:
        post = Post(
            caption="First post!",
            url="https://example.com/image.jpg",
            file_type="image/jpeg",
            file_name="image.jpg"
        )
        session.add(post)
        await session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
