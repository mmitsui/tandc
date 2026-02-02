"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    api_title: str = "ToS Clarity API"
    api_version: str = "v1"
    api_prefix: str = "/api"
    debug: bool = False
    
    # Database Settings
    database_url: str = "postgresql://postgres:postgres@localhost:5432/tosclarity"
    database_echo: bool = False
    
    # Redis Settings
    redis_url: str = "redis://localhost:6379/0"
    redis_ttl_seconds: int = 3600  # 1 hour default cache TTL
    
    # Anthropic API Settings
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    
    # CORS Settings
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
