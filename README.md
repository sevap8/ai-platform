# AI Platform - Production Ready Framework

This is a production-ready framework for an AI Platform built with LangChain and Qdrant. The architecture follows clean, modular design principles to facilitate easy extension and maintenance.

## Project Structure

```
ai-platform/
├── api/                    # API layer with FastAPI endpoints
│   ├── __init__.py
│   └── routers.py
├── core/                   # Core entities and interfaces
│   ├── __init__.py
│   ├── entities.py         # Data models
│   └── interfaces.py       # Abstract interfaces
├── services/               # Business logic services
│   ├── __init__.py
│   └── storage_manager.py
├── vector_store/           # Vector storage implementations
│   ├── __init__.py
│   └── qdrant_impl.py
├── config/                 # Configuration management
│   ├── __init__.py
│   └── settings.py
├── utils/                  # Utility functions
│   ├── __init__.py
│   └── document_processor.py
├── models/                 # ML/AI models (placeholder)
│   └── __init__.py
├── main.py                 # Application entry point
├── README.md               # This file
├── requirements.txt        # Python dependencies
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

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python -m ai_platform.main
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `POST /upload`: Upload a document file
- `POST /retrieve`: Retrieve documents based on a query
- `GET /health`: Check application health status

## Configuration

Application settings are managed in `config/settings.py` and can be overridden using environment variables or a `.env` file.

Key settings include:
- Qdrant connection parameters
- Application settings
- Document processing limits