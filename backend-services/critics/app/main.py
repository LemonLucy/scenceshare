from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import engine, Base, get_db
from app.models import CriticsReview

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Critics Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.get("/reviews")
def get_reviews(
    movie_id: int = None,
    critic_type: str = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(CriticsReview)
    if movie_id:
        query = query.filter(CriticsReview.movie_id == movie_id)
    if critic_type:
        query = query.filter(CriticsReview.critic_type == critic_type)
    
    reviews = query.order_by(desc(CriticsReview.created_at)).offset(skip).limit(limit).all()
    return reviews

@router.get("/reviews/{review_id}")
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(CriticsReview).filter(CriticsReview.id == review_id).first()
    if not review:
        return {"error": "Review not found"}
    
    review.view_count += 1
    db.commit()
    return review

app.include_router(router, prefix="/api/v1/critics", tags=["Critics"])

@app.get("/")
def root():
    return {"service": "Critics", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
