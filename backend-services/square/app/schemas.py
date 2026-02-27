from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PostCreate(BaseModel):
    movie_id: Optional[int] = None
    movie_title: Optional[str] = None
    movie_poster: Optional[str] = None
    title: str
    content: str
    post_type: str = "discussion"
    username: str = "Anonymous"

class PostResponse(BaseModel):
    id: int
    user_id: int
    username: str
    movie_id: Optional[int]
    movie_title: Optional[str]
    movie_poster: Optional[str]
    title: str
    content: str
    post_type: str
    view_count: int
    like_count: int
    comment_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str
    username: str = "Anonymous"

class CommentResponse(BaseModel):
    id: int
    post_id: int
    username: str
    content: str
    like_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostWithComments(PostResponse):
    comments: List[CommentResponse] = []
