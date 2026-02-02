"""Tests for API dependencies."""
import pytest
from sqlalchemy.orm import Session
from app.api.dependencies import get_db


def test_get_db(db_session: Session):
    """Test database dependency."""
    db_gen = get_db()
    db = next(db_gen)
    
    assert isinstance(db, Session)
    
    # Cleanup
    try:
        next(db_gen)
    except StopIteration:
        pass
