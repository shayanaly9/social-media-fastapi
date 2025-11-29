from pydantic import BaseModel
import uuid

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: uuid.UUID
    caption: str
    url: str
    file_type: str
    file_name: str
    created_at: str
