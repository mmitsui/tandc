"""Pytest configuration and fixtures."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from redis.asyncio import Redis
from app.main import app
from app.models.database import Base
from app.api.dependencies import get_db, get_redis
from app.config import settings

# Test database URL (in-memory SQLite for tests)
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def db_session():
    """Create a test database session."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session):
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
async def mock_redis():
    """Mock Redis client for testing."""
    # In a real test, you might use fakeredis or a test Redis instance
    # For now, we'll just override the dependency
    class MockRedis:
        async def ping(self):
            return True
        
        async def setex(self, key, ttl, value):
            return True
        
        async def get(self, key):
            return None
        
        async def delete(self, key):
            return True
    
    async def override_get_redis():
        return MockRedis()
    
    app.dependency_overrides[get_redis] = override_get_redis
    yield MockRedis()
    app.dependency_overrides.clear()
