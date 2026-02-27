from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ArchiveInterview

router = APIRouter()

@router.get("/interviews")
def get_interviews(
    movie_id: int = None,
    role: str = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get interviews"""
    query = db.query(ArchiveInterview)
    if movie_id:
        query = query.filter(ArchiveInterview.movie_id == movie_id)
    if role:
        query = query.filter(ArchiveInterview.interviewee_role == role)
    
    interviews = query.order_by(ArchiveInterview.created_at.desc()).offset(skip).limit(limit).all()
    return interviews
