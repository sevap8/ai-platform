# AI Platform - Production Ready Framework

This is a production-ready framework for an AI Platform built with LangChain and Qdrant. The architecture follows clean, modular design principles to facilitate easy extension and maintenance.

## Project Structure

```
ai-platform/
├── api/                    # API layer with FastAPI endpoints
│   └── routers.py
├── core/                   # Core entities and interfaces
│   ├── entities.py         # Core data models
│   └── interfaces.py       # Abstract interfaces
├── services/               # Business logic services
│   └── storage_manager.py
├── vector_store/           # Vector storage implementations
│   └── qdrant_impl.py
├── utils/                  # Utility functions
│   └── document_processor.py
├── main.py                 # Application entry point
├── README.md               # This file
├── pyproject.toml          # Project configuration for uv
├── .env.example            # Example environment variables
└── __init__.py             # Package initialization
```

## Key Components

### Core Entities (`core/entities.py`)
- `Document`: Represents a document in the system
- `QueryResult`: Represents a result from a retrieval query
- `UploadResponse`: Response model for document upload operations
- `RetrieveResponse`: Response model for document retrieval operations

### Interfaces (`core/interfaces.py`)
- `VectorStoreInterface`: Contract for vector storage operations
- `DocumentProcessorInterface`: Contract for document processing operations
- `StorageManagerInterface`: Contract for storage management operations

### API Layer (`api/routers.py`)
- `/upload`: Endpoint for uploading documents
- `/retrieve`: Endpoint for retrieving documents based on queries
- `/health`: Health check endpoint

### Services (`services/storage_manager.py`)
- `StorageManager`: Orchestrates document storage and retrieval operations

### Vector Store (`vector_store/qdrant_impl.py`)
- `QdrantVectorStore`: Concrete implementation of vector storage using Qdrant

## Features

1. **Modular Architecture**: Clean separation of concerns with well-defined interfaces
2. **Extensible Design**: Easy to add new vector stores, document processors, etc.
3. **Production Ready**: Includes proper error handling, configuration management, and health checks
4. **API Ready**: Pre-configured FastAPI endpoints for document upload and retrieval

## Usage

1. Copy the environment variables file:
```bash
cp .env.example .env
```

Then update the values in `.env` as needed.

2. Install dependencies using uv:
```bash
uv sync
```

Or install directly:
```bash
uv pip install langchain qdrant-client fastapi uvicorn pydantic python-multipart
```

3. Run the application:
```bash
uv run uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

After starting the application, you can access:

- `http://127.0.0.1:8000/docs` - Interactive API documentation (Swagger UI)
- `http://127.0.0.1:8000/redoc` - Alternative API documentation (ReDoc)
- `http://127.0.0.1:8000/health` - Health check endpoint

## API Endpoints

- `POST /upload`: Upload a document file
- `POST /retrieve`: Retrieve documents based on a query
- `GET /health`: Check application health status

## Configuration

Application settings are managed through environment variables defined in the `.env` file.

Key settings include:
- Qdrant connection parameters
- Application settings
- Document processing limits