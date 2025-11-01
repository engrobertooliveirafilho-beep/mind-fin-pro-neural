# app/schemas/post.py
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(PostCreate):
    id: int
    author_id: int

    class Config:
        from_attributes = True  # (antes era orm_mode=True no Pydantic v1)
