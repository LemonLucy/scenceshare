from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./sceneshare.db"
    TMDB_API_KEY: str = ""
    YOUTUBE_API_KEY: str = ""
    JWT_SECRET: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"

settings = Settings()
