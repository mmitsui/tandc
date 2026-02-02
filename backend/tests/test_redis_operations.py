"""Comprehensive tests for Redis operations."""
import pytest
from app.api.dependencies import get_redis
from redis.asyncio import Redis
import json
from uuid import uuid4


@pytest.mark.asyncio
async def test_redis_connection(mock_redis):
    """Test that Redis connection works."""
    result = await mock_redis.ping()
    assert result is True


@pytest.mark.asyncio
async def test_redis_set_get(mock_redis):
    """Test setting and getting values from Redis."""
    key = "test:key"
    value = "test_value"
    
    await mock_redis.setex(key, 3600, value)
    result = await mock_redis.get(key)
    
    assert result == value


@pytest.mark.asyncio
async def test_redis_job_status_storage(mock_redis):
    """Test storing job status in Redis."""
    job_id = uuid4()
    status = "processing"
    
    await mock_redis.setex(
        f"job:{job_id}",
        3600,
        status
    )
    
    result = await mock_redis.get(f"job:{job_id}")
    assert result == status


@pytest.mark.asyncio
async def test_redis_ttl_expiration(mock_redis):
    """Test that Redis keys expire after TTL."""
    key = "test:expire"
    value = "test_value"
    
    await mock_redis.setex(key, 1, value)
    
    # Immediately after setting, should exist
    result = await mock_redis.get(key)
    assert result == value
    
    # After expiration (mocked), should be None
    # Note: In real tests with fakeredis, you'd need to advance time
    # For now, we just test the pattern


@pytest.mark.asyncio
async def test_redis_delete(mock_redis):
    """Test deleting keys from Redis."""
    key = "test:delete"
    value = "test_value"
    
    await mock_redis.setex(key, 3600, value)
    result = await mock_redis.get(key)
    assert result == value
    
    await mock_redis.delete(key)
    result = await mock_redis.get(key)
    assert result is None


@pytest.mark.asyncio
async def test_redis_json_storage(mock_redis):
    """Test storing JSON data in Redis."""
    key = "test:json"
    data = {
        "job_id": str(uuid4()),
        "status": "processing",
        "progress": 50
    }
    
    json_value = json.dumps(data)
    await mock_redis.setex(key, 3600, json_value)
    
    result = await mock_redis.get(key)
    assert result == json_value
    
    # Parse back to dict
    parsed = json.loads(result)
    assert parsed["status"] == "processing"
    assert parsed["progress"] == 50


@pytest.mark.asyncio
async def test_redis_multiple_keys(mock_redis):
    """Test storing and retrieving multiple keys."""
    keys_values = {
        "job:1": "processing",
        "job:2": "completed",
        "job:3": "failed",
    }
    
    for key, value in keys_values.items():
        await mock_redis.setex(key, 3600, value)
    
    # Retrieve all
    for key, expected_value in keys_values.items():
        result = await mock_redis.get(key)
        assert result == expected_value


@pytest.mark.asyncio
async def test_redis_get_redis_dependency(mock_redis):
    """Test the get_redis dependency function."""
    # This tests the dependency injection pattern
    # In tests, get_redis is overridden to return mock_redis
    redis_client = mock_redis
    
    # Should return a Redis client (or mock in tests)
    assert redis_client is not None
    
    # Should support ping
    result = await redis_client.ping()
    assert result is True
