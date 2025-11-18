# Project Structure

## Overview
Professional FastAPI application for generating QA pairs from PDF documents.

## Directory Structure

```
qa-pipeline/
├── app/                    # Main application package
│   ├── api/               # API layer
│   │   ├── __init__.py
│   │   └── routes.py      # API endpoints (POST /generate-qa, GET /health)
│   ├── core/              # Business logic
│   │   ├── __init__.py
│   │   ├── config.py      # Configuration management (.env loading)
│   │   └── pipeline.py    # QA generation pipeline
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   └── schemas.py     # Pydantic validation schemas
│   ├── __init__.py
│   └── main.py            # FastAPI application entry point
├── tests/                 # Test files
│   └── test_api.py        # API endpoint tests
├── .env                   # Environment variables (not in git)
├── .env.example           # Example environment file
├── .gitignore             # Git ignore rules
├── README.md              # Documentation
├── requirements.txt       # Python dependencies
└── run.py                 # Application runner
```

## Key Components

### app/main.py
- FastAPI application initialization
- Router registration
- Application metadata

### app/api/routes.py
- API endpoint definitions
- Request/response handling
- Thread pool executor for async operations

### app/core/pipeline.py
- QA generation pipeline
- PDF text extraction
- Text chunking
- LLM integration

### app/core/config.py
- Environment variable loading
- Configuration validation

### app/models/schemas.py
- Pydantic models for validation
- Request/response schemas

## Running the Application

```bash
# Development mode with auto-reload
python run.py

# Production mode
python -m app.main
```

## Testing

```bash
# Start server
python run.py

# Run tests (in another terminal)
python tests/test_api.py
```

## API Endpoints

- `POST /generate-qa` - Generate QA pairs from PDF
- `GET /health` - Health check

## Configuration

Set these in `.env`:
- `MODEL_NAME` - LLM model name
- `API_BASE` - API base URL
- `API_KEY` - API authentication key
