"""Tests for summary API endpoint."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.database import Document, Summary
import hashlib
from uuid import uuid4


def test_get_summary_not_found(client: TestClient):
    """Test getting a summary that doesn't exist."""
    fake_id = uuid4()
    response = client.get(f"/api/summary/{fake_id}")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_summary_success(client: TestClient, db_session: Session):
    """Test getting an existing summary."""
    # Create document
    content = "This is test content"
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    document = Document(
        url="https://example.com/tos",
        service_name="Example Service",
        document_type="tos",
        raw_content=content,
        content_hash=content_hash,
    )
    
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)
    
    # Create summary
    summary = Summary(
        document_id=document.id,
        version=1,
        red_flags=[
            {
                "severity": "warning",
                "category": "data_sharing",
                "title": "Broad Data Sharing",
                "explanation": "Your data may be shared with third parties",
                "source_quote": "We may share your data..."
            }
        ],
        rules=[
            {
                "category": "content",
                "title": "No Harmful Content",
                "description": "You may not post harmful content",
                "consequence": "Account termination"
            }
        ],
        concessions=[
            {
                "category": "data",
                "title": "Data Collection",
                "what_you_give": "Personal information",
                "why_they_want_it": "To provide services",
                "can_opt_out": False,
                "opt_out_instructions": None
            }
        ],
        clarity_score=75,
        reading_level="High School",
        original_word_count=1000,
        summary_word_count=200,
        model_version="claude-3-5-sonnet-20241022",
    )
    
    db_session.add(summary)
    db_session.commit()
    db_session.refresh(summary)
    
    # Get summary via API
    response = client.get(f"/api/summary/{summary.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(summary.id)
    assert data["service_name"] == "Example Service"
    assert data["document_type"] == "tos"
    assert data["clarity_score"] == 75
    assert len(data["red_flags"]) == 1
    assert len(data["rules"]) == 1
    assert len(data["concessions"]) == 1
    assert "metadata" in data
