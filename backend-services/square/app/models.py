from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class SquarePost(Base):
    __tablename__ = "square_posts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String(100), default="Anonymous")
    movie_id = Column(Integer, nullable=True)  # None = 전체 게시판
    movie_title = Column(String(500))
    movie_poster = Column(String(500))
    title = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    post_type = Column(String(20), default="discussion")  # discussion, review, question
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("square_posts.id", ondelete="CASCADE"))
    user_id = Column(Integer, nullable=False)
    username = Column(String(100), default="Anonymous")
    content = Column(Text, nullable=False)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    post = relationship("SquarePost", back_populates="comments")
