"""
Service layer for the AI Platform.

This module contains business logic services that coordinate between
different components of the application.
"""

from typing import List
from core.interfaces import StorageManagerInterface, VectorStoreInterface
from core.entities import Document, QueryResult
from utils.document_processor import process_uploaded_file


class StorageManager(StorageManagerInterface):
    """
    Main service class that manages document storage and retrieval operations.

    This service coordinates between document processing, vector storage,
    and other components to provide unified storage functionality.
    """

    def __init__(self):
        """
        Initialize the storage manager.
        """
        self.vector_store: VectorStoreInterface = None  # Will be initialized later

    async def initialize(self):
        """
        Initialize the storage manager and its dependencies.
        """
        from vector_store.qdrant_impl import QdrantVectorStore
        self.vector_store = QdrantVectorStore()
        await self.vector_store._ensure_collection_exists()

    async def store_document_from_file(self, file, document_id: str) -> bool:
        """
        Store a document from an uploaded file.

        Args:
            file: Uploaded file object
            document_id: ID to assign to the document

        Returns:
            True if successful, False otherwise
        """
        # Read file data
        file_data = await file.read()
        filename = file.filename

        # Process the document using the simplified function
        documents = await process_uploaded_file(file_data, filename)

        # Add processed documents to vector store
        success = True
        for doc in documents:
            # Override the ID with the provided document_id
            doc.id = document_id
            add_success = await self.vector_store.add_document(doc)
            if not add_success:
                success = False

        return success

    async def store_document(self, document: Document) -> bool:
        """
        Store a processed document in the system.

        Args:
            document: The document to store

        Returns:
            True if successful, False otherwise
        """
        return await self.vector_store.add_document(document)

    async def retrieve_documents(self, query: str, top_k: int = 5) -> List[QueryResult]:
        """
        Retrieve documents based on a query.

        Args:
            query: The search query
            top_k: Number of top results to return

        Returns:
            List of matching documents with scores
        """
        return await self.vector_store.search(query, top_k)