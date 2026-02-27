from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SquarePost
from app.schemas import PostCreate, PostResponse

router = APIRouter()

@router.get("/posts", response_model=List[PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get all posts"""
    posts = db.query(SquarePost).order_by(SquarePost.created_at.desc()).offset(skip).limit(limit).all()
    return posts

@router.post("/posts", response_model=PostResponse)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db)
):
    """Create a new post"""
    # TODO: Add authentication
    db_post = SquarePost(
        user_id=1,  # Temporary user_id
        **post.dict()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get post by ID"""
    post = db.query(SquarePost).filter(SquarePost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.view_count += 1
    db.commit()
    return post
