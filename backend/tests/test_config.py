"""Tests for configuration."""
import pytest
from app.config import settings


def test_settings_loaded():
    """Test that settings are loaded."""
    assert settings.api_title == "ToS Clarity API"
    assert settings.api_version == "v1"
    assert settings.api_prefix == "/api"
    assert settings.database_url is not None
    assert settings.redis_url is not None


def test_cors_origins():
    """Test CORS origins configuration."""
    assert isinstance(settings.cors_origins, list)
    assert len(settings.cors_origins) > 0
