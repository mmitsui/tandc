# ToS Clarity Backend

FastAPI backend for the ToS Clarity application.

## Setup

### Prerequisites
- Python 3.11+
- Poetry (for dependency management)
- Docker & Docker Compose (for PostgreSQL and Redis)

### Installation

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp ../.env.example ../.env
# Edit .env with your configuration
```

3. Start PostgreSQL and Redis:
```bash
docker-compose up -d
```

4. Run database migrations:
```bash
poetry run alembic upgrade head
```

5. Start the development server:
```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

## Testing

Run tests with pytest:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov=app --cov-report=html
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes and dependencies
│   ├── models/           # Database models and schemas
│   ├── services/         # Business logic services
│   ├── utils/            # Utility functions
│   ├── prompts/          # AI prompt templates
│   ├── config.py         # Configuration
│   └── main.py           # FastAPI application
├── alembic/              # Database migrations
├── tests/                # Unit and integration tests
└── pyproject.toml        # Dependencies and project config
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/analyze` - Submit URL for analysis
- `GET /api/summary/{id}` - Get analysis summary
- `POST /api/compare` - Compare multiple summaries

See `/docs` for interactive API documentation.
