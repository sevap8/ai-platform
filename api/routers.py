"""
API layer for the AI Platform.

This module implements the REST API endpoints for document upload and retrieval.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from typing import List
import uuid
from core.entities import UploadResponse, RetrieveResponse, QueryResult
from services.storage_manager import StorageManager
from config.settings import get_settings


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
    
    # Initialize services
    settings = get_settings()
    storage_manager = StorageManager(settings)
    
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
            
            # Save file temporarily and process it
            # (Actual implementation will be added later)
            success = await storage_manager.store_document_from_file(file, document_id)
            
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
    
    @app.post("/retrieve", response_model=RetrieveResponse)
    async def retrieve_documents(query: str, top_k: int = 5):
        """
        Retrieve documents based on a query.
        
        Args:
            query: The search query
            top_k: Number of top results to return (default: 5)
            
        Returns:
            RetrieveResponse with matching documents
        """
        try:
            results = await storage_manager.retrieve_documents(query, top_k)
            return RetrieveResponse(results=results, query=query)
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