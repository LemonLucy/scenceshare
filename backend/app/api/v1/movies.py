from fastapi import APIRouter
from app.services.tmdb import tmdb_service

router = APIRouter()

@router.get("/trending")
async def get_trending(time_window: str = "week", page: int = 1):
    """Get trending movies from TMDB"""
    return await tmdb_service.get_trending(time_window, page)

@router.get("/search")
async def search_movies(q: str, page: int = 1):
    """Search movies"""
    return await tmdb_service.search_movies(q, page)

@router.get("/{movie_id}")
async def get_movie(movie_id: int):
    """Get movie details"""
    return await tmdb_service.get_movie(movie_id)
