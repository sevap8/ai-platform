"""
Qdrant vector store implementation for the AI Platform.

This module provides concrete implementation using Qdrant as the vector database.
"""

import os
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from core.entities import Document, QueryResult
import uuid
from typing import List


class QdrantVectorStore:
    """
    Qdrant vector store implementation.

    This class provides methods to interact with Qdrant for storing and retrieving
    document embeddings.
    """

    def __init__(self):
        """
        Initialize the Qdrant vector store.
        """
        url = os.getenv("QDRANT_URL", "localhost")
        port = int(os.getenv("QDRANT_PORT", 6333))
        api_key = os.getenv("QDRANT_API_KEY")

        # Determine if we should use HTTPS based on the presence of API key or explicit HTTPS URL
        https = api_key is not None and len(api_key) > 0

        # Create client with appropriate configuration
        if url.startswith("https://") or url.startswith("http://"):
            # If URL includes protocol, use it as-is
            self.client = AsyncQdrantClient(url=url, api_key=api_key)
        elif https:
            # Use HTTPS connection
            self.client = AsyncQdrantClient(url=url, port=port, api_key=api_key, https=True)
        else:
            # Use HTTP connection
            self.client = AsyncQdrantClient(url=url, port=port, api_key=api_key, https=False)

        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "documents")

    async def _ensure_collection_exists(self):
        """
        Ensure that the collection exists in Qdrant.
        """
        # For now, just print a message instead of interacting with Qdrant
        print(f"Ensuring collection '{self.collection_name}' exists (simulated)")

    async def add_document(self, document: Document) -> bool:
        """
        Add a document to the vector store.

        Args:
            document: The document to add

        Returns:
            True if successful, False otherwise
        """
        # For now, just print the content to console instead of saving to Qdrant
        content_preview = document.content[:100] if len(document.content) > 100 else document.content
        print(f"Document content preview (first 100 chars): {content_preview}")
        print(f"Document metadata: {document.metadata}")
        print(f"Document ID: {document.id}")

        # Temporary: return True to indicate success without actually storing
        return True

    async def search(self, query: str, top_k: int = 5) -> List[QueryResult]:
        """
        Search for similar documents to the query.

        Args:
            query: The search query
            top_k: Number of top results to return

        Returns:
            List of matching documents with scores
        """
        # For now, return empty results since we're not actually storing documents
        print(f"Search query: {query}, top_k: {top_k}")
        return []

    async def delete_document(self, document_id: str) -> bool:
        """
        Delete a document from the vector store.

        Args:
            document_id: ID of the document to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[document_id]
                )
            )
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False