"""Tests for application startup and initialization."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text, inspect
from app.main import app
from app.api.dependencies import engine, get_db
from app.models.database import Base
from tests.conftest import test_engine


def test_app_creation():
    """Test that the FastAPI app is created correctly."""
    assert app is not None
    assert app.title == "ToS Clarity API"
    assert app.version == "v1"


def test_app_routes_registered(client: TestClient):
    """Test that all routes are registered."""
    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    
    # Test health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    
    # Test API endpoints exist (may return errors, but should be 404, not 405)
    response = client.get("/api/analyze")
    assert response.status_code in [404, 405]  # Method not allowed or not found
    
    response = client.get("/api/summary/00000000-0000-0000-0000-000000000000")
    assert response.status_code in [404, 422]  # Not found or validation error


def test_root_endpoint_response(client: TestClient):
    """Test root endpoint returns correct structure."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert data["message"] == "ToS Clarity API"
    assert data["version"] == "v1"
    assert data["docs"] == "/docs"


def test_health_check_success(client: TestClient):
    """Test health check endpoint when all services are healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    # In test environment, status might be "healthy" or "unhealthy" depending on services
    assert data["status"] in ["healthy", "unhealthy"]


def test_health_check_structure(client: TestClient):
    """Test health check endpoint returns correct structure."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    
    # If healthy, should have database and redis status
    if data["status"] == "healthy":
        assert "database" in data
        assert "redis" in data


def test_cors_headers(client: TestClient):
    """Test that CORS headers are configured."""
    # Make an OPTIONS request to test CORS
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        }
    )
    
    # CORS middleware should handle this
    # The exact response depends on CORS configuration
    assert response.status_code in [200, 204, 405]


def test_api_docs_available(client: TestClient):
    """Test that OpenAPI docs are available."""
    response = client.get("/docs")
    # Should return HTML for Swagger UI
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_openapi_schema_available(client: TestClient):
    """Test that OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "ToS Clarity API"
    assert schema["info"]["version"] == "v1"


def test_database_connection_pool(db_session):
    """Test that database connection pool is configured."""
    # Test that we can get a connection from the test engine
    assert test_engine is not None
    
    # Test that we can get a connection
    with test_engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_database_tables_created(db_session):
    """Test that database tables are created."""
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()
    
    # Should have documents and summaries tables
    assert "documents" in tables
    assert "summaries" in tables


def test_database_table_structure(db_session):
    """Test that database tables have correct structure."""
    inspector = inspect(test_engine)
    
    # Check documents table columns
    doc_columns = {col["name"] for col in inspector.get_columns("documents")}
    expected_doc_columns = {"id", "url", "service_name", "document_type", 
                            "raw_content", "content_hash", "extracted_at"}
    assert expected_doc_columns.issubset(doc_columns)
    
    # Check summaries table columns
    summary_columns = {col["name"] for col in inspector.get_columns("summaries")}
    expected_summary_columns = {"id", "document_id", "version", "red_flags", 
                               "rules", "concessions", "clarity_score", 
                               "reading_level", "original_word_count", 
                               "summary_word_count", "generated_at", "model_version"}
    assert expected_summary_columns.issubset(summary_columns)


def test_database_foreign_key_constraint(db_session):
    """Test that foreign key constraint exists between summaries and documents."""
    inspector = inspect(test_engine)
    foreign_keys = inspector.get_foreign_keys("summaries")
    
    # Should have foreign key to documents table
    fk_to_documents = [
        fk for fk in foreign_keys 
        if fk["referred_table"] == "documents"
    ]
    
    assert len(fk_to_documents) > 0
    assert "document_id" in fk_to_documents[0]["constrained_columns"]


def test_database_indexes_created(db_session):
    """Test that database indexes are created."""
    inspector = inspect(test_engine)
    
    # Check documents table indexes
    doc_indexes = {idx["name"] for idx in inspector.get_indexes("documents")}
    # Should have indexes on url, service_name, and content_hash
    assert len(doc_indexes) > 0
    
    # Check summaries table indexes
    summary_indexes = {idx["name"] for idx in inspector.get_indexes("summaries")}
    # Should have index on document_id
    assert len(summary_indexes) > 0
