"""
Qdrant vector store implementation for the AI Platform.

This module provides concrete implementation of the VectorStoreInterface
using Qdrant as the vector database.
"""

import os
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from core.interfaces import VectorStoreInterface
from core.entities import Document, QueryResult
import uuid
from typing import List


class QdrantVectorStore(VectorStoreInterface):
    """
    Qdrant implementation of the VectorStoreInterface.

    This class provides methods to interact with Qdrant for storing and retrieving
    document embeddings.
    """

    def __init__(self):
        """
        Initialize the Qdrant vector store.
        """
        self.client = AsyncQdrantClient(
            url=os.getenv("QDRANT_URL", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333)),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "documents")

    async def _ensure_collection_exists(self):
        """
        Ensure that the collection exists in Qdrant.
        """
        try:
            collections = (await self.client.get_collections()).collections
            collection_names = [collection.name for collection in collections]

            if self.collection_name not in collection_names:
                # Create collection with appropriate settings
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)  # Using 768 dimensions as expected by Qdrant
                )
        except Exception as e:
            print(f"Error ensuring collection exists: {e}")

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

        # Temporarily skip saving to Qdrant
        # In a real implementation, we would generate embeddings here
        # For now, we'll use a mock embedding (zeros array)
        # In production, you would use an embedding model to generate actual embeddings
        # mock_embedding = [0.0] * 768  # Mock embedding vector - Qdrant expects 768 dimensions

        # Prepare the record to insert
        # records = [
        #     models.PointStruct(
        #         id=document.id if document.id != "" else str(uuid.uuid4()),
        #         vector=mock_embedding,
        #         payload={
        #             "content": document.content,
        #             "metadata": document.metadata,
        #             "created_at": document.created_at.isoformat()
        #         }
        #     )
        # ]

        # Insert the record into Qdrant
        # await self.client.upsert(
        #     collection_name=self.collection_name,
        #     points=records
        # )

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
        try:
            # In a real implementation, we would generate an embedding for the query
            # and perform a vector similarity search
            # For now, we'll return empty results as a placeholder
            # since we don't have an actual embedding model integrated

            # In a real implementation, you would:
            # 1. Generate embedding for the query
            # 2. Perform vector similarity search
            # 3. Return the results

            # For demonstration purposes, returning empty list
            # In a real implementation, this would return actual search results
            return []
        except Exception as e:
            print(f"Error searching documents: {e}")
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