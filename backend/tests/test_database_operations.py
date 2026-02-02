"""Comprehensive tests for database operations."""
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.database import Document, Summary
import hashlib
from datetime import datetime, timezone


def test_document_creation_with_all_fields(db_session: Session):
    """Test creating a document with all required fields."""
    content = "Test Terms of Service content"
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    document = Document(
        url="https://example.com/terms",
        service_name="Example Service",
        document_type="tos",
        raw_content=content,
        content_hash=content_hash,
    )
    
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)
    
    assert document.id is not None
    assert document.url == "https://example.com/terms"
    assert document.service_name == "Example Service"
    assert document.document_type == "tos"
    assert document.raw_content == content
    assert document.content_hash == content_hash
    assert document.extracted_at is not None
    assert isinstance(document.extracted_at, datetime)


def test_document_unique_content_hash(db_session: Session):
    """Test that documents can have the same content hash (different URLs)."""
    content = "Same content"
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    doc1 = Document(
        url="https://example.com/tos",
        service_name="Example",
        document_type="tos",
        raw_content=content,
        content_hash=content_hash,
    )
    
    doc2 = Document(
        url="https://example.com/privacy",
        service_name="Example",
        document_type="privacy",
        raw_content=content,
        content_hash=content_hash,
    )
    
    db_session.add_all([doc1, doc2])
    db_session.commit()
    
    # Both should be saved successfully
    assert doc1.id != doc2.id
    assert doc1.content_hash == doc2.content_hash


def test_document_different_types(db_session: Session):
    """Test creating documents with different document types."""
    content = "Test content"
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    types = ["tos", "privacy", "community_guidelines", "other"]
    documents = []
    
    for doc_type in types:
        doc = Document(
            url=f"https://example.com/{doc_type}",
            service_name="Example",
            document_type=doc_type,
            raw_content=content,
            content_hash=content_hash,
        )
        documents.append(doc)
    
    db_session.add_all(documents)
    db_session.commit()
    
    assert len(documents) == 4
    for doc in documents:
        assert doc.id is not None


def test_summary_creation_with_json_fields(db_session: Session):
    """Test creating a summary with JSON fields properly populated."""
    # Create document first
    content = "Test content"
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    document = Document(
        url="https://example.com/tos",
        service_name="Example",
        document_type="tos",
        raw_content=content,
        content_hash=content_hash,
    )
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)
    
    # Create summary with complex JSON data
    red_flags = [
        {
            "severity": "critical",
            "category": "arbitration",
            "title": "Mandatory Arbitration",
            "explanation": "You waive your right to a jury trial",
            "source_quote": "All disputes must be resolved through arbitration"
        }
    ]
    
    rules = [
        {
            "category": "content",
            "title": "No Illegal Content",
            "description": "You may not post illegal content",
            "consequence": "Account termination and legal action"
        }
    ]
    
    concessions = [
        {
            "category": "data",
            "title": "Data Collection",
            "what_you_give": "Personal information and usage data",
            "why_they_want_it": "To improve services and for advertising",
            "can_opt_out": True,
            "opt_out_instructions": "Visit settings > privacy"
        }
    ]
    
    summary = Summary(
        document_id=document.id,
        version=1,
        red_flags=red_flags,
        rules=rules,
        concessions=concessions,
        clarity_score=65,
        reading_level="College",
        original_word_count=5000,
        summary_word_count=350,
        model_version="claude-3-5-sonnet-20241022",
    )
    
    db_session.add(summary)
    db_session.commit()
    db_session.refresh(summary)
    
    assert summary.id is not None
    assert len(summary.red_flags) == 1
    assert len(summary.rules) == 1
    assert len(summary.concessions) == 1
    assert summary.red_flags[0]["severity"] == "critical"
    assert summary.concessions[0]["can_opt_out"] is True


def test_summary_versioning(db_session: Session):
    """Test that multiple summaries can exist for the same document."""
    # Create document
    content = "Test content"
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    document = Document(
        url="https://example.com/tos",
        service_name="Example",
        document_type="tos",
        raw_content=content,
        content_hash=content_hash,
    )
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)
    
    # Create multiple summaries with different versions
    summaries = []
    for version in range(1, 4):
        summary = Summary(
            document_id=document.id,
            version=version,
            red_flags=[],
            rules=[],
            concessions=[],
            clarity_score=70 + version,
            reading_level="High School",
            original_word_count=1000,
            summary_word_count=200,
            model_version="claude-3-5-sonnet-20241022",
        )
        summaries.append(summary)
    
    db_session.add_all(summaries)
    db_session.commit()
    db_session.refresh(document)
    
    assert len(document.summaries) == 3
    versions = {s.version for s in document.summaries}
    assert versions == {1, 2, 3}


def test_document_cascade_delete(db_session: Session):
    """Test that deleting a document cascades to delete its summaries."""
    # Create document
    content = "Test content"
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    document = Document(
        url="https://example.com/tos",
        service_name="Example",
        document_type="tos",
        raw_content=content,
        content_hash=content_hash,
    )
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)
    
    # Create summaries
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
    
    summary_ids = [summary1.id, summary2.id]
    
    # Delete document
    db_session.delete(document)
    db_session.commit()
    
    # Verify summaries are also deleted
    remaining_summaries = db_session.query(Summary).filter(
        Summary.id.in_(summary_ids)
    ).all()
    
    assert len(remaining_summaries) == 0


def test_summary_requires_document(db_session: Session):
    """Test that a summary cannot be created without a valid document_id."""
    fake_document_id = "550e8400-e29b-41d4-a716-446655440000"
    
    summary = Summary(
        document_id=fake_document_id,
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
    
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_document_query_by_service_name(db_session: Session):
    """Test querying documents by service name."""
    services = ["YouTube", "OpenAI", "YouTube", "OpenAI"]
    documents = []
    
    for i, service in enumerate(services):
        content = f"Content for {service}"
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        doc = Document(
            url=f"https://{service.lower()}.com/tos",
            service_name=service,
            document_type="tos",
            raw_content=content,
            content_hash=content_hash,
        )
        documents.append(doc)
    
    db_session.add_all(documents)
    db_session.commit()
    
    # Query by service name
    youtube_docs = db_session.query(Document).filter(
        Document.service_name == "YouTube"
    ).all()
    
    assert len(youtube_docs) == 2
    assert all(doc.service_name == "YouTube" for doc in youtube_docs)


def test_document_query_by_content_hash(db_session: Session):
    """Test querying documents by content hash."""
    content = "Shared content"
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    doc1 = Document(
        url="https://example.com/tos",
        service_name="Example",
        document_type="tos",
        raw_content=content,
        content_hash=content_hash,
    )
    
    doc2 = Document(
        url="https://example.com/privacy",
        service_name="Example",
        document_type="privacy",
        raw_content=content,
        content_hash=content_hash,
    )
    
    db_session.add_all([doc1, doc2])
    db_session.commit()
    
    # Query by content hash
    matching_docs = db_session.query(Document).filter(
        Document.content_hash == content_hash
    ).all()
    
    assert len(matching_docs) == 2
    assert all(doc.content_hash == content_hash for doc in matching_docs)
