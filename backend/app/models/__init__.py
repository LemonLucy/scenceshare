from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    overview = Column(Text)
    poster_path = Column(String(500))
    backdrop_path = Column(String(500))
    release_date = Column(String(50))
    vote_average = Column(Float)
    genres = Column(JSON)
    tmdb_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    square_posts = relationship("SquarePost", back_populates="movie")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    square_posts = relationship("SquarePost", back_populates="user")

class SquarePost(Base):
    __tablename__ = "square_posts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    title = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    post_type = Column(String(20), default="discussion")
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="square_posts")
    movie = relationship("Movie", back_populates="square_posts")

class CriticsReview(Base):
    __tablename__ = "critics_reviews"
    
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    critic_name = Column(String(200), nullable=False)
    critic_type = Column(String(50))
    youtube_video_id = Column(String(50))
    rating = Column(Float)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class ArchiveInterview(Base):
    __tablename__ = "archive_interviews"
    
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    title = Column(String(500), nullable=False)
    interviewee_name = Column(String(200), nullable=False)
    interviewee_role = Column(String(100))
    youtube_video_id = Column(String(50))
    description = Column(Text)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
