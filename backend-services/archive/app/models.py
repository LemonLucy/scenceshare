from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.database import Base

class ArchiveInterview(Base):
    __tablename__ = "archive_interviews"
    
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer)
    movie_title = Column(String(500))
    title = Column(String(500), nullable=False)
    interviewee_name = Column(String(200), nullable=False)
    interviewee_role = Column(String(100))  # director, actor, producer
    youtube_video_id = Column(String(50))
    source_url = Column(String(500))
    description = Column(Text)
    tags = Column(JSON)
    duration = Column(String(20))
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
