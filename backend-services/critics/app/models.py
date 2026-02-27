from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from datetime import datetime
from app.database import Base

class CriticsReview(Base):
    __tablename__ = "critics_reviews"
    
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, nullable=False)
    movie_title = Column(String(500))
    critic_name = Column(String(200), nullable=False)
    critic_type = Column(String(50))  # professional, youtuber, blogger
    source_name = Column(String(200))
    youtube_video_id = Column(String(50))
    rating = Column(Float)
    summary = Column(Text)
    full_text = Column(Text)
    tags = Column(JSON)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
