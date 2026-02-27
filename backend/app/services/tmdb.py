import httpx
from typing import Optional, Dict, Any
from app.config import settings

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"
    
    async def get_trending(self, time_window: str = "week", page: int = 1) -> Dict[str, Any]:
        """Get trending movies"""
        if not settings.TMDB_API_KEY:
            return {"results": [], "page": 1, "total_pages": 0}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/trending/movie/{time_window}",
                    params={"api_key": settings.TMDB_API_KEY, "page": page}
                )
                response.raise_for_status()
                return response.json()
            except:
                return {"results": [], "page": 1, "total_pages": 0}
    
    async def search_movies(self, query: str, page: int = 1) -> Dict[str, Any]:
        """Search movies"""
        if not settings.TMDB_API_KEY:
            return {"results": [], "page": 1, "total_pages": 0}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/search/movie",
                    params={"api_key": settings.TMDB_API_KEY, "query": query, "page": page}
                )
                response.raise_for_status()
                return response.json()
            except:
                return {"results": [], "page": 1, "total_pages": 0}
    
    async def get_movie(self, movie_id: int) -> Dict[str, Any]:
        """Get movie details"""
        if not settings.TMDB_API_KEY:
            return {}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/movie/{movie_id}",
                    params={"api_key": settings.TMDB_API_KEY}
                )
                response.raise_for_status()
                return response.json()
            except:
                return {}

tmdb_service = TMDBService()
