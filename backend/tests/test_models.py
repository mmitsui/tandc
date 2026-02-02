"""Tests for database models."""
import pytest
from sqlalchemy.orm import Session
from app.models.database import Document, Summary
from datetime import datetime
import hashlib


def test_create_document(db_session: Session):
    """Test creating a document."""
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
    
    assert document.id is not None
    assert document.service_name == "Example Service"
    assert document.document_type == "tos"
    assert document.content_hash == content_hash


def test_create_summary(db_session: Session):
    """Test creating a summary."""
    # First create a document
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
        red_flags=[],
        rules=[],
        concessions=[],
        clarity_score=75,
        reading_level="High School",
        original_word_count=1000,
        summary_word_count=200,
        model_version="claude-3-5-sonnet-20241022",
    )
    
    db_session.add(summary)
    db_session.commit()
    db_session.refresh(summary)
    
    assert summary.id is not None
    assert summary.document_id == document.id
    assert summary.clarity_score == 75
    assert len(document.summaries) == 1
    assert document.summaries[0].id == summary.id


def test_document_summary_relationship(db_session: Session):
    """Test document-summary relationship."""
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
    
    # Create multiple summaries
    summary1 = Summary(
        document_id=document.id,
        version=1,
        red_flags=[],
        rules=[],
        concessions=[],
        clarity_score=75,
        reading_level="High School",
        original_word_count=1000,
        summary_word_count=200,
        model_version="claude-3-5-sonnet-20241022",
    )
    
    summary2 = Summary(
        document_id=document.id,
        version=2,
        red_flags=[],
        rules=[],
        concessions=[],
        clarity_score=80,
        reading_level="High School",
        original_word_count=1000,
        summary_word_count=180,
        model_version="claude-3-5-sonnet-20241022",
    )
    
    db_session.add_all([summary1, summary2])
    db_session.commit()
    db_session.refresh(document)
    
    assert len(document.summaries) == 2
    assert {s.version for s in document.summaries} == {1, 2}
