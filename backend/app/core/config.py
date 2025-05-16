from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    # TMDB API settings
    tmdb_api_key: str
    tmdb_api_base_url: str = "https://api.themoviedb.org/3/"
    tmdb_image_base_url: str = "https://image.tmdb.org/t/p"
    
    # Authentication settings
    secret_key: str = "your-secret-key-here"  # Change this in production!
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database settings (to be implemented)
    database_url: str = "sqlite:///./movie_recommender.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
