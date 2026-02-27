from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api.v1 import movies, square, critics, archive

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SceneShare API",
    description="Global Movie Community API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(movies.router, prefix="/api/v1/movies", tags=["Movies"])
app.include_router(square.router, prefix="/api/v1/square", tags=["Square"])
app.include_router(critics.router, prefix="/api/v1/critics", tags=["Critics"])
app.include_router(archive.router, prefix="/api/v1/archive", tags=["Archive"])

@app.get("/")
def root():
    return {
        "message": "Welcome to SceneShare API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
