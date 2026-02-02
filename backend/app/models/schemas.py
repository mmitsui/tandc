"""Pydantic schemas for API requests and responses."""
from pydantic import BaseModel, Field, HttpUrl
from typing import Literal, Optional
from datetime import datetime
from uuid import UUID


class RedFlagSchema(BaseModel):
    """Red flag schema."""
    severity: Literal["critical", "warning", "info"]
    category: str
    title: str
    explanation: str
    source_quote: str
    
    class Config:
        from_attributes = True


class RuleSchema(BaseModel):
    """Rule schema."""
    category: str
    title: str
    description: str
    consequence: Optional[str] = None
    
    class Config:
        from_attributes = True


class ConcessionSchema(BaseModel):
    """Concession schema."""
    category: str
    title: str
    what_you_give: str
    why_they_want_it: str
    can_opt_out: bool
    opt_out_instructions: Optional[str] = None
    
    class Config:
        from_attributes = True


class DocumentSchema(BaseModel):
    """Document schema."""
    id: UUID
    url: str
    service_name: str
    document_type: str
    content_hash: str
    extracted_at: datetime
    
    class Config:
        from_attributes = True


class SummarySchema(BaseModel):
    """Summary schema."""
    id: UUID
    document_id: UUID
    version: int
    red_flags: list[RedFlagSchema]
    rules: list[RuleSchema]
    concessions: list[ConcessionSchema]
    clarity_score: int
    reading_level: str
    original_word_count: int
    summary_word_count: int
    generated_at: datetime
    model_version: str
    
    class Config:
        from_attributes = True


class AnalyzeRequest(BaseModel):
    """Request schema for analyze endpoint."""
    url: HttpUrl
    options: Optional[dict] = Field(default_factory=dict)


class AnalyzeResponse(BaseModel):
    """Response schema for analyze endpoint."""
    job_id: UUID
    status: str
    estimated_time_seconds: int


class SummaryResponse(BaseModel):
    """Response schema for summary endpoint."""
    id: UUID
    service_name: str
    document_type: str
    analyzed_at: datetime
    clarity_score: int
    red_flags: list[RedFlagSchema]
    rules: list[RuleSchema]
    concessions: list[ConcessionSchema]
    metadata: dict
