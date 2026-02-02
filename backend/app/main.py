"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.config import settings
from app.api.dependencies import get_db, get_redis, engine
from app.models.database import Base
from app.api.routes import analyze, summary, compare


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        debug=settings.debug,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(analyze.router, prefix=settings.api_prefix, tags=["analyze"])
    app.include_router(summary.router, prefix=settings.api_prefix, tags=["summary"])
    app.include_router(compare.router, prefix=settings.api_prefix, tags=["compare"])
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize database and Redis connections on startup."""
        # Create database tables
        Base.metadata.create_all(bind=engine)
        # Test Redis connection
        redis_client = await get_redis()
        await redis_client.ping()
    
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "ToS Clarity API",
            "version": settings.api_version,
            "docs": "/docs",
        }
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        try:
            # Check database
            db = next(get_db())
            db.execute(text("SELECT 1"))
            db.close()
            
            # Check Redis
            redis_client = await get_redis()
            await redis_client.ping()
            
            return {"status": "healthy", "database": "connected", "redis": "connected"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    return app


app = create_app()
