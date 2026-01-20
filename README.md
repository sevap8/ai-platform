# AI Platform - Production Ready Framework

This is a production-ready framework for an AI Platform built with LangChain and Qdrant. The architecture follows clean, modular design principles to facilitate easy extension and maintenance.

## Project Structure

```
ai-platform/
├── api/                    # API layer with FastAPI endpoints
│   └── routers.py
├── core/                   # Core entities
│   └── entities.py         # Core data models
├── services/               # Business logic services
│   └── storage_manager.py
├── vector_store/           # Vector storage implementations
│   └── qdrant_impl.py
├── infrastructure/         # Infrastructure components
│   └── file_loader.py      # LangChain-compatible file loader
├── processors/             # Data processing components
│   └── file_processor.py   # File processing utilities
├── main.py                 # Application entry point
├── README.md               # This file
├── pyproject.toml          # Project configuration for uv
├── .env.example            # Example environment variables
└── __init__.py             # Package initialization
```

## Project Architecture

The project is organized based on principles of modularity and separation of concerns. Each layer has a clear purpose and dependencies, which simplifies maintenance and extension of the code.

### Directory Structure

- `core` — contains entities and base classes representing the domain.
- `api` — presentation layer, request routing.
- `services` — business logic layer, coordinating work between different components.
- `infrastructure` — infrastructure layer, providing interaction with external systems and databases.
- `processors` — data processing layer, specific to the application.
- `utils` — utility functions for general use, used in different parts of the application.

### Design Principles

- **Separation of Concerns**: each layer is responsible for its own functional area.
- **Modularity**: components are easily replaceable and reusable.
- **Flexibility and Scalability**: the architecture allows for easy addition of new features without disrupting existing logic.

## Key Components

### Core Entities (`core/entities.py`)
- `Document`: Represents a document in the system
- `QueryResult`: Represents a result from a retrieval query
- `UploadResponse`: Response model for document upload operations
- `RetrieveResponse`: Response model for document retrieval operations


### API Layer (`api/routers.py`)
- `/upload`: Endpoint for uploading documents
- `/retrieve`: Endpoint for retrieving documents based on queries
- `/health`: Health check endpoint

### Services (`services/storage_manager.py`)
- `StorageManager`: Orchestrates document storage and retrieval operations

### Vector Store (`vector_store/qdrant_impl.py`)
- `QdrantVectorStore`: Concrete implementation of vector storage using Qdrant

## Features

1. **Simple Architecture**: Clean and straightforward design without unnecessary abstractions
2. **Extensible Design**: Easy to add new vector stores, document processors, etc.
3. **Production Ready**: Includes proper error handling, configuration management, and health checks
4. **API Ready**: Pre-configured FastAPI endpoints for document upload and retrieval
5. **Multi-format Support**: Handles various file formats including PDF, Excel, text files, JSON, YAML, XML, and more
6. **LangChain Integration**: Built with LangChain compatibility for advanced document processing
7. **Configurable Text Chunking**: Adjustable parameters for splitting documents into chunks for better processing

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

### General Application Settings
- `APP_HOST`: Host address for the application (default: 0.0.0.0)
- `APP_PORT`: Port for the application (default: 8000)
- `APP_RELOAD`: Enable/disable auto-reload on code changes (default: true)

### Qdrant Settings
- `QDRANT_URL`: URL for Qdrant server (default: localhost)
- `QDRANT_PORT`: Port for Qdrant server (default: 6333)
- `QDRANT_API_KEY`: API key for Qdrant (optional)
- `QDRANT_COLLECTION_NAME`: Name of the collection in Qdrant (default: documents)

### Document Processing Settings
- `MAX_FILE_SIZE_MB`: Maximum allowed file size in MB (default: 10)
- `ALLOWED_EXTENSIONS`: Comma-separated list of allowed file extensions (optional, uses default if not set)

### Text Chunking Settings
- `CHUNK_SIZE`: Size of text chunks in characters (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks in characters (default: 200)
- `SEPARATOR`: Separator character for splitting text (default: \n)

To customize these settings:
1. Copy the example file: `cp .env.example .env`
2. Modify the values in `.env` as needed
3. Restart the application for changes to take effect