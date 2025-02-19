# backend/app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Base API configs
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Spark Tutorial API"
    
    # Google OAuth configs
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_OAUTH_URL: str = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL: str = "https://www.googleapis.com/oauth2/v1/userinfo"
    
    # Frontend URL for CORS
    FRONTEND_URL: str = "http://localhost:3000"
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-replace-in-production"  # replace in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()