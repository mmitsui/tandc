"""Analyze endpoint routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_redis
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from uuid import uuid4
from redis.asyncio import Redis

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_url(
    request: AnalyzeRequest,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """
    Submit a URL for analysis.
    
    Returns a job ID that can be used to retrieve the analysis results.
    """
    job_id = uuid4()
    
    # Store job status in Redis
    await redis.setex(
        f"job:{job_id}",
        3600,  # 1 hour TTL
        "processing"
    )
    
    # TODO: Queue actual analysis job (Phase 1 - Document Extraction Service)
    
    return AnalyzeResponse(
        job_id=job_id,
        status="processing",
        estimated_time_seconds=15,
    )
