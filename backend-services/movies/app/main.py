from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="Movies Service (TMDB)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "7394c0d4d8e4eb4b65728ea9d83ff3d8")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

@app.get("/")
def root():
    return {"service": "Movies", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/v1/movies/trending")
async def get_trending(time_window: str = "week", page: int = 1):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{TMDB_BASE_URL}/trending/movie/{time_window}",
                params={"api_key": TMDB_API_KEY, "page": page}
            )
            response.raise_for_status()
            return response.json()
        except:
            return {"results": [], "page": 1, "total_pages": 0}

@app.get("/api/v1/movies/search")
async def search_movies(q: str, page: int = 1):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{TMDB_BASE_URL}/search/movie",
                params={"api_key": TMDB_API_KEY, "query": q, "page": page}
            )
            response.raise_for_status()
            return response.json()
        except:
            return {"results": [], "page": 1, "total_pages": 0}

@app.get("/api/v1/movies/{movie_id}")
async def get_movie(movie_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{TMDB_BASE_URL}/movie/{movie_id}",
                params={"api_key": TMDB_API_KEY}
            )
            response.raise_for_status()
            return response.json()
        except:
            return {}

@app.get("/api/v1/movies/{movie_id}/reviews")
async def get_movie_reviews(movie_id: int, page: int = 1):
    """영화 리뷰 가져오기 (TMDB)"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{TMDB_BASE_URL}/movie/{movie_id}/reviews",
                params={"api_key": TMDB_API_KEY, "page": page}
            )
            response.raise_for_status()
            return response.json()
        except:
            return {"results": [], "page": 1, "total_pages": 0}
