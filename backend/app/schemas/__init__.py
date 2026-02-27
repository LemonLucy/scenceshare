from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MovieBase(BaseModel):
    title: str
    overview: Optional[str] = None
    poster_path: Optional[str] = None

class MovieResponse(MovieBase):
    id: int
    vote_average: Optional[float] = None
    release_date: Optional[str] = None
    
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    movie_id: Optional[int] = None
    title: str
    content: str
    post_type: str = "discussion"

class PostResponse(BaseModel):
    id: int
    user_id: int
    movie_id: Optional[int]
    title: str
    content: str
    post_type: str
    view_count: int
    like_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    display_name: Optional[str]
    
    class Config:
        from_attributes = True
