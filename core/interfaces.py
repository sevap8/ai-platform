"""
Interface definitions for the AI Platform.

This module contains abstract base classes that define contracts
for various components of the system.
"""

from abc import ABC, abstractmethod
from typing import List
from .entities import Document, QueryResult


class VectorStoreInterface(ABC):
    """
    Abstract interface for vector storage operations.
    
    This interface defines the contract for vector storage implementations,
    allowing for different backends like Qdrant, Pinecone, etc.
    """
    
    @abstractmethod
    async def add_document(self, document: Document) -> bool:
        """
        Add a document to the vector store.
        
        Args:
            document: The document to add
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def search(self, query: str, top_k: int = 5) -> List[QueryResult]:
        """
        Search for similar documents to the query.
        
        Args:
            query: The search query
            top_k: Number of top results to return
            
        Returns:
            List of matching documents with scores
        """
        pass
    
    @abstractmethod
    async def delete_document(self, document_id: str) -> bool:
        """
        Delete a document from the vector store.
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            True if successful, False otherwise
        """
        pass




class StorageManagerInterface(ABC):
    """
    Abstract interface for storage management operations.
    
    This interface defines the contract for managing document storage
    and retrieval operations.
    """
    
    @abstractmethod
    async def store_document(self, document: Document) -> bool:
        """
        Store a processed document in the system.
        
        Args:
            document: The document to store
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def retrieve_documents(self, query: str, top_k: int = 5) -> List[QueryResult]:
        """
        Retrieve documents based on a query.
        
        Args:
            query: The search query
            top_k: Number of top results to return
            
        Returns:
            List of matching documents with scores
        """
        pass