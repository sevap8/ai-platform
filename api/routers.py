"""
API layer for the AI Platform.

This module implements the REST API endpoints for document upload and retrieval.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import List
import uuid
from core.entities import UploadResponse, RetrieveResponse, QueryResult
from services.storage_manager import StorageManager


# Global variable to hold the storage manager instance
storage_manager = None


def get_storage_manager():
    """
    Get the storage manager instance, initializing it if necessary.
    """
    global storage_manager
    if storage_manager is None:
        storage_manager = StorageManager()
    return storage_manager


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="AI Platform API",
        description="Production-ready API for document upload and retrieval",
        version="1.0.0"
    )

    @app.on_event("startup")
    async def startup():
        """
        Initialize services when the application starts.
        """
        sm = get_storage_manager()
        await sm.initialize()

    @app.post("/upload", response_model=UploadResponse)
    async def upload_document(file: UploadFile = File(...)):
        """
        Upload a document to the system.

        Args:
            file: The document file to upload

        Returns:
            UploadResponse with document ID and status
        """
        try:
            # Generate unique document ID
            document_id = str(uuid.uuid4())

            # Get the storage manager instance
            sm = get_storage_manager()

            # Save file temporarily and process it
            success = await sm.store_document_from_file(file, document_id)

            if success:
                return UploadResponse(
                    document_id=document_id,
                    status="success",
                    message=f"Document {document_id} uploaded successfully"
                )
            else:
                raise HTTPException(status_code=500, detail="Failed to store document")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    @app.get("/health")
    async def health_check():
        """
        Health check endpoint to verify API is running.

        Returns:
            Simple status message
        """
        return {"status": "healthy"}

    return app


# Create the main application instance
app = create_app()