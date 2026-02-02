"""Compare endpoint routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from typing import List
from uuid import UUID

router = APIRouter()


@router.post("/compare")
async def compare_services(
    summary_ids: List[UUID],
    db: Session = Depends(get_db),
):
    """
    Compare multiple service summaries.
    
    TODO: Implement comparison logic (Phase 3)
    """
    return {"message": "Comparison feature coming soon", "summary_ids": summary_ids}
