from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import CriticsReview

router = APIRouter()

@router.get("/reviews")
def get_reviews(
    movie_id: int = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get critic reviews"""
    query = db.query(CriticsReview)
    if movie_id:
        query = query.filter(CriticsReview.movie_id == movie_id)
    
    reviews = query.order_by(CriticsReview.created_at.desc()).offset(skip).limit(limit).all()
    return reviews
