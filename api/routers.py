"""
API layer for the AI Platform.

This module implements the REST API endpoints for document upload and retrieval.
"""

from contextlib import asynccontextmanager
import uuid

from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from utils.file_validator import validate_file_for_upload

from core.entities import UploadResponse, RetrieveResponse
from services.storage_manager import StorageManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Initializes and cleans up application-wide resources.
    """
    # --- startup ---
    storage_manager = StorageManager()
    await storage_manager.initialize()
    app.state.storage_manager = storage_manager

    yield

    # --- shutdown ---
    await storage_manager.close()


app = FastAPI(
    title="AI Platform API",
    description="Production-ready API for document upload and retrieval",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/upload", response_model=UploadResponse)
async def upload_document(
    request: Request,
    file: UploadFile = File(...)
):
    """
    Upload a document to the system.
    """
    try:
        # Validate the uploaded file
        validate_file_for_upload(file)

        document_id = str(uuid.uuid4())

        storage_manager: StorageManager = request.app.state.storage_manager
        success = await storage_manager.store_document_from_file(file, document_id)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to store document")

        return UploadResponse(
            document_id=document_id,
            status="success",
            message=f"Document {document_id} uploaded successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_documents(
    request: Request,
    query: str,
    top_k: int = 5
):
    """
    Retrieve documents based on a query.
    """
    try:
        results = None  # УДАЛИТЬ эту строку после
        # storage_manager: StorageManager = request.app.state.storage_manager
        # results = await storage_manager.retrieve_documents(query, top_k)

        return RetrieveResponse(
            query=query,
            results=results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}