"""SQLAlchemy database models."""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class Document(Base):
    """Document model for storing extracted ToS/Privacy Policy documents."""
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, nullable=False, index=True)
    service_name = Column(String, nullable=False, index=True)
    document_type = Column(String, nullable=False)  # "tos", "privacy", "community_guidelines", "other"
    raw_content = Column(Text, nullable=False)
    content_hash = Column(String, nullable=False, index=True)  # For detecting changes
    extracted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    summaries = relationship("Summary", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(id={self.id}, service_name={self.service_name}, type={self.document_type})>"


class Summary(Base):
    """Summary model for storing AI-generated summaries."""
    __tablename__ = "summaries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False, index=True)
    version = Column(Integer, nullable=False, default=1)
    
    # Structured summary sections stored as JSON
    red_flags = Column(JSON, nullable=False, default=list)
    rules = Column(JSON, nullable=False, default=list)
    concessions = Column(JSON, nullable=False, default=list)
    
    # Metadata
    clarity_score = Column(Integer, nullable=False)  # 0-100
    reading_level = Column(String, nullable=False)  # e.g., "College", "High School"
    original_word_count = Column(Integer, nullable=False)
    summary_word_count = Column(Integer, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    model_version = Column(String, nullable=False)
    
    # Relationships
    document = relationship("Document", back_populates="summaries")
    
    def __repr__(self):
        return f"<Summary(id={self.id}, document_id={self.document_id}, clarity_score={self.clarity_score})>"
