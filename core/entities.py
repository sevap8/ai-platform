"""
Core entities for the AI Platform.

This module defines the fundamental data structures used throughout the application.
"""

from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class Document(BaseModel):
    """
    Represents a document in the system.
    
    Attributes:
        id: Unique identifier for the document
        content: The actual content of the document
        metadata: Additional information about the document
        created_at: Timestamp when the document was created
    """
    id: str
    content: str
    metadata: Dict[str, Any] = {}
    created_at: datetime = datetime.now()


class QueryResult(BaseModel):
    """
    Represents a result from a retrieval query.
    
    Attributes:
        document_id: ID of the matched document
        content: Content of the matched document
        score: Relevance score of the match
        metadata: Metadata associated with the document
    """
    document_id: str
    content: str
    score: float
    metadata: Dict[str, Any] = {}


class UploadResponse(BaseModel):
    """
    Response model for document upload operations.
    
    Attributes:
        document_id: ID of the uploaded document
        status: Status of the upload operation
        message: Human-readable message about the operation
    """
    document_id: str
    status: str
    message: str


class RetrieveResponse(BaseModel):
    """
    Response model for document retrieval operations.
    
    Attributes:
        results: List of matching documents
        query: The original query that was performed
    """
    results: list[QueryResult]
    query: str