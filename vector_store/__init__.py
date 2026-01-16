"""
Factory and interface implementations for vector stores.

This module provides factory functions to create vector store instances
and any additional implementations beyond Qdrant.
"""

from core.interfaces import VectorStoreInterface
from .qdrant_impl import QdrantVectorStore
from config.settings import Settings


def create_vector_store(settings: Settings) -> VectorStoreInterface:
    """
    Factory function to create a vector store instance based on configuration.
    
    Args:
        settings: Application settings containing vector store configuration
        
    Returns:
        Instance of a VectorStoreInterface implementation
    """
    # Currently only Qdrant is supported, but this could be extended
    # to support other vector databases like Pinecone, Weaviate, etc.
    return QdrantVectorStore(settings)


__all__ = ["create_vector_store", "QdrantVectorStore"]