"""
Simplified document processing for the AI Platform.

This module provides a streamlined approach to document processing without
unnecessary abstractions.
"""

from typing import List
import tempfile
import os
from pathlib import Path
from core.entities import Document
from .file_loader import FileLoader


async def process_uploaded_file(file_data: bytes, filename: str) -> List[Document]:
    """
    Process an uploaded file and return parsed documents.

    Args:
        file_data: Raw file data
        filename: Name of the uploaded file

    Returns:
        List of extracted documents
    """
    # Create a temporary file to work with
    file_extension = Path(filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(file_data)
        tmp_file_path = tmp_file.name

    try:
        # Use the FileLoader to process the file directly
        loader = FileLoader(file_path=tmp_file_path)
        lc_docs = loader.load()

        # Convert LangChain documents to our core Document entities
        documents = []
        for i, lc_doc in enumerate(lc_docs):
            doc_id = f"{Path(tmp_file_path).stem}_{i}" if len(lc_docs) > 1 else Path(tmp_file_path).stem
            document = Document(
                id=doc_id,
                content=lc_doc.page_content,
                metadata={**lc_doc.metadata, "source": filename}
            )
            documents.append(document)

        return documents
    finally:
        # Clean up the temporary file
        os.unlink(tmp_file_path)