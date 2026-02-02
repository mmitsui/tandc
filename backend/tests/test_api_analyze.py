"""Tests for analyze API endpoint."""
import pytest
from fastapi.testclient import TestClient


def test_analyze_endpoint(client: TestClient):
    """Test analyze endpoint."""
    response = client.post(
        "/api/analyze",
        json={
            "url": "https://www.youtube.com/static?template=terms",
            "options": {}
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert "status" in data
    assert "estimated_time_seconds" in data
    assert data["status"] == "processing"


def test_analyze_endpoint_invalid_url(client: TestClient):
    """Test analyze endpoint with invalid URL."""
    response = client.post(
        "/api/analyze",
        json={
            "url": "not-a-valid-url",
            "options": {}
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_missing_url(client: TestClient):
    """Test analyze endpoint with missing URL."""
    response = client.post(
        "/api/analyze",
        json={
            "options": {}
        }
    )
    
    assert response.status_code == 422  # Validation error
