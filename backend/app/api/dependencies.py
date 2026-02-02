"""API dependencies for dependency injection."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from redis.asyncio import Redis, from_url
from app.config import settings
from typing import AsyncGenerator, Generator

# Database setup
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

__all__ = ["engine", "get_db", "get_redis"]

# Redis client (singleton)
_redis_client: Redis | None = None


def get_db() -> Generator[Session, None, None]:
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_redis() -> Redis:
    """Dependency for getting Redis client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = await from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client
