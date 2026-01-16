"""
Document processing implementations for the AI Platform.

This module provides concrete implementations of document processing interfaces.
"""

from typing import List
from pathlib import Path
import tempfile
from core.interfaces import DocumentProcessorInterface
from core.entities import Document


class SimpleDocumentProcessor(DocumentProcessorInterface):
    """
    Simple implementation of the DocumentProcessorInterface.
    
    This class provides basic document processing capabilities.
    In a real implementation, this would include parsing different file formats,
    extracting text, and chunking documents appropriately.
    """
    
    async def process_document(self, file_path: str) -> List[Document]:
        """
        Process a document file and extract its content.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of extracted documents
        """
        # In a real implementation, we would parse the file based on its type
        # and extract the content. For now, we'll simulate this process.
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create a document from the content
        # In a real implementation, we might split large documents into chunks
        document = Document(
            id=file_path.split("/")[-1],  # Use filename as ID for simplicity
            content=content,
            metadata={"source": file_path, "processed_by": "SimpleDocumentProcessor"}
        )
        
        return [document]


class DocumentProcessingService:
    """
    Service class that manages document processing operations.
    
    This service acts as an orchestrator for document processing tasks,
    coordinating between different processors and handling file operations.
    """
    
    def __init__(self, processor: DocumentProcessorInterface):
        """
        Initialize the document processing service.
        
        Args:
            processor: Document processor implementation to use
        """
        self.processor = processor
    
    async def process_uploaded_file(self, file_data: bytes, filename: str) -> List[Document]:
        """
        Process an uploaded file and return parsed documents.
        
        Args:
            file_data: Raw file data
            filename: Name of the uploaded file
            
        Returns:
            List of extracted documents
        """
        # Create a temporary file to work with
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp_file:
            tmp_file.write(file_data)
            tmp_file_path = tmp_file.name
        
        try:
            # Process the temporary file
            documents = await self.processor.process_document(tmp_file_path)
            return documents
        finally:
            # Clean up the temporary file
            import os
            os.unlink(tmp_file_path)