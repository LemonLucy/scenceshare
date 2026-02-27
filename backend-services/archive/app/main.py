from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import engine, Base, get_db
from app.models import ArchiveInterview

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Archive Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.get("/interviews")
def get_interviews(
    movie_id: int = None,
    role: str = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(ArchiveInterview)
    if movie_id:
        query = query.filter(ArchiveInterview.movie_id == movie_id)
    if role:
        query = query.filter(ArchiveInterview.interviewee_role == role)
    
    interviews = query.order_by(desc(ArchiveInterview.created_at)).offset(skip).limit(limit).all()
    return interviews

@router.get("/interviews/{interview_id}")
def get_interview(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(ArchiveInterview).filter(ArchiveInterview.id == interview_id).first()
    if not interview:
        return {"error": "Interview not found"}
    
    interview.view_count += 1
    db.commit()
    return interview

app.include_router(router, prefix="/api/v1/archive", tags=["Archive"])

@app.get("/")
def root():
    return {"service": "Archive", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
