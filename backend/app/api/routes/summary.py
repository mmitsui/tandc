"""Summary endpoint routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models.schemas import SummaryResponse
from app.models.database import Summary, Document
from uuid import UUID

router = APIRouter()


@router.get("/summary/{summary_id}", response_model=SummaryResponse)
async def get_summary(
    summary_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve a summary by ID.
    """
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    document = db.query(Document).filter(Document.id == summary.document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Convert JSON columns to Pydantic models
    from app.models.schemas import RedFlagSchema, RuleSchema, ConcessionSchema
    
    return SummaryResponse(
        id=summary.id,
        service_name=document.service_name,
        document_type=document.document_type,
        analyzed_at=summary.generated_at,
        clarity_score=summary.clarity_score,
        red_flags=[RedFlagSchema(**flag) for flag in summary.red_flags],
        rules=[RuleSchema(**rule) for rule in summary.rules],
        concessions=[ConcessionSchema(**concession) for concession in summary.concessions],
        metadata={
            "original_word_count": summary.original_word_count,
            "summary_word_count": summary.summary_word_count,
            "reading_level": summary.reading_level,
            "model_version": summary.model_version,
        },
    )
