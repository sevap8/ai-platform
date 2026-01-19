"""
File processing utilities for the AI Platform.

This module handles file uploads and conversion to Document entities.
"""

from typing import List
import tempfile
import os
from pathlib import Path
from core.entities import Document
from infrastructure.file_loader import FileLoader
import asyncio
import aiofiles
from utils.file_validator import validate_file_type



class FileProcessor:
    """
    Handles parallel processing of files with error handling.
    """
    def __init__(self, concurrency: int = 1, silent_errors: bool = False):
        """
        Initialize the FileProcessor.

        Args:
            concurrency: Number of concurrent file processing tasks
            silent_errors: Whether to suppress errors during processing
        """
        self.concurrency = concurrency
        self.silent_errors = silent_errors
        self.semaphore = asyncio.Semaphore(concurrency)

    async def process_files(self, file_paths: List[str]) -> List[Document]:
        """
        Process multiple files in parallel.

        Args:
            file_paths: List of paths to files to process

        Returns:
            List of processed documents
        """
        tasks = [self._process_single_file(file_path) for file_path in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten results and handle exceptions
        all_docs = []
        for result in results:
            if isinstance(result, Exception):
                if not self.silent_errors:
                    raise result
            else:
                all_docs.extend(result)

        return all_docs

    async def _process_single_file(self, file_path: str) -> List[Document]:
        """
        Process a single file with semaphore control.

        Args:
            file_path: Path to the file to process

        Returns:
            List of processed documents
        """
        async with self.semaphore:
            try:
                loader = FileLoader(file_path=file_path)
                docs = loader.load()
                return docs
            except Exception as e:
                if not self.silent_errors:
                    raise e
                return []


async def process_uploaded_file(file_data: bytes, filename: str, concurrency: int = 1, silent_errors: bool = False) -> List[Document]:
    """
    Process an uploaded file and return parsed documents.

    Args:
        file_data: Raw file data
        filename: Name of the uploaded file

    Returns:
        List of extracted documents
    """
    # Validate file type before processing
    if not validate_file_type(filename):
        if not silent_errors:
            raise ValueError(f"Unsupported file type: {Path(filename).suffix}")
        return []

    # Create a temporary file to work with
    file_extension = Path(filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(file_data)
        tmp_file_path = tmp_file.name

    try:
        # Use the FileProcessor to process the file
        processor = FileProcessor(concurrency=concurrency, silent_errors=silent_errors)
        docs = await processor.process_files([tmp_file_path])

        # Convert LangChain documents to our core Document entities
        documents = []
        for i, lc_doc in enumerate(docs):
            doc_id = f"{Path(tmp_file_path).stem}_{i}" if len(docs) > 1 else Path(tmp_file_path).stem
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