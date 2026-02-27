from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
import httpx
from app.database import get_db
from app.models import SquarePost, Comment
from app.schemas import (
    PostCreate, PostResponse, PostWithComments,
    CommentCreate, CommentResponse
)

router = APIRouter()

# 인증 체크 함수
async def verify_auth(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    
    # Auth 서비스에 토큰 검증 요청
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://localhost:8004/api/v1/auth/me?token={token}"
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
            return response.json()
        except:
            raise HTTPException(status_code=401, detail="Authentication failed")

# ===== Posts =====

@router.get("/posts", response_model=List[PostResponse])
def get_posts(
    sort: str = Query("recent", regex="^(recent|popular)$"),
    movie_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    게시글 목록 조회
    - sort=recent: 최신순 (전체)
    - sort=popular: 인기순 (좋아요 많은 순, 전체)
    - movie_id: 특정 영화 게시글만
    """
    query = db.query(SquarePost)
    
    # 영화별 필터
    if movie_id:
        query = query.filter(SquarePost.movie_id == movie_id)
    
    # 정렬
    if sort == "popular":
        query = query.order_by(desc(SquarePost.like_count), desc(SquarePost.created_at))
    else:  # recent
        query = query.order_by(desc(SquarePost.created_at))
    
    posts = query.offset(skip).limit(limit).all()
    return posts

@router.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """게시글 작성"""
    db_post = SquarePost(
        user_id=1,  # TODO: 실제 인증된 user_id
        username=post.username,
        movie_id=post.movie_id,
        movie_title=post.movie_title,
        movie_poster=post.movie_poster,
        title=post.title,
        content=post.content,
        post_type=post.post_type
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts/{post_id}", response_model=PostWithComments)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_auth)  # 로그인 필수
):
    """게시글 상세 (댓글 포함) - 로그인 필요"""
    post = db.query(SquarePost).filter(SquarePost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 조회수 증가
    post.view_count += 1
    db.commit()
    db.refresh(post)
    
    return post

@router.post("/posts/{post_id}/like")
def like_post(post_id: int, db: Session = Depends(get_db)):
    """게시글 좋아요"""
    post = db.query(SquarePost).filter(SquarePost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.like_count += 1
    db.commit()
    return {"like_count": post.like_count}

@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """게시글 삭제"""
    post = db.query(SquarePost).filter(SquarePost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}

# ===== Comments =====

@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """댓글 목록"""
    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(Comment.created_at).all()
    return comments

@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    """댓글 작성"""
    # 게시글 존재 확인
    post = db.query(SquarePost).filter(SquarePost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 댓글 생성
    db_comment = Comment(
        post_id=post_id,
        user_id=1,  # TODO: 실제 user_id
        username=comment.username,
        content=comment.content
    )
    db.add(db_comment)
    
    # 게시글 댓글 수 증가
    post.comment_count += 1
    
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.post("/comments/{comment_id}/like")
def like_comment(comment_id: int, db: Session = Depends(get_db)):
    """댓글 좋아요"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    comment.like_count += 1
    db.commit()
    return {"like_count": comment.like_count}

# ===== Stats =====

@router.get("/stats/movies")
def get_movie_stats(db: Session = Depends(get_db)):
    """영화별 게시글 통계 (인기 영화)"""
    stats = db.query(
        SquarePost.movie_id,
        SquarePost.movie_title,
        SquarePost.movie_poster,
        func.count(SquarePost.id).label('post_count')
    ).filter(
        SquarePost.movie_id.isnot(None)
    ).group_by(
        SquarePost.movie_id,
        SquarePost.movie_title,
        SquarePost.movie_poster
    ).order_by(
        desc('post_count')
    ).limit(10).all()
    
    return [
        {
            "movie_id": s.movie_id,
            "movie_title": s.movie_title,
            "movie_poster": s.movie_poster,
            "post_count": s.post_count
        }
        for s in stats
    ]
