from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # ===== Application =====
    APP_NAME: str = "News Dashboard API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # ===== News API =====
    NEWS_API_KEY: str = ""
    NEWS_API_BASE_URL: str = "https://newsapi.org/v2"
    
    # ===== Database =====
    POSTGRES_USER: str = "news_user"
    POSTGRES_PASSWORD: str = "news_password"
    POSTGRES_DB: str = "news_dashboard"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    
    @property
    def DATABASE_URL(self) -> str:
        """Generate PostgreSQL connection URL"""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # ===== Redis =====
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    REDIS_DECODE_RESPONSES: bool = True
    
    @property
    def REDIS_URL(self) -> str:
        """Generate Redis connection URL"""
        if self.REDIS_PASSWORD:
            return (
                f"redis://:{self.REDIS_PASSWORD}"
                f"@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
            )
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # ===== Cache TTL (seconds) =====
    CACHE_TTL_DEFAULT: int = 300
    CACHE_TTL_NEWS: int = 180
    CACHE_TTL_USER: int = 600
    
    # ===== CORS =====
    CORS_ORIGINS: str = '["http://localhost:4200", "http://localhost:4300"]'
    
    @property
    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from string to list"""
        try:
            origins = json.loads(self.CORS_ORIGINS)
            return origins if isinstance(origins, list) else [self.CORS_ORIGINS]
        except:
            # Fallback to default origins
            return ["http://localhost:4200", "http://localhost:4300"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env


# Create settings instance
settings = Settings()


# Debug: Print loaded settings (optional, remove in production)
if settings.DEBUG:
    import sys
    if "pytest" not in sys.modules:  # Don't print during tests
        print(f"📋 Loaded settings:")
        print(f"   APP_NAME: {settings.APP_NAME}")
        print(f"   APP_VERSION: {settings.APP_VERSION}")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   POSTGRES_HOST: {settings.POSTGRES_HOST}")
        print(f"   REDIS_HOST: {settings.REDIS_HOST}")
        print(f"   CACHE_TTL_NEWS: {settings.CACHE_TTL_NEWS}s")
        print(f"   CORS_ORIGINS: {settings.get_cors_origins}")
