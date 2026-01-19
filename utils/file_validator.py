"""
File validation utilities for the AI Platform.

This module provides utility functions for validating uploaded files
according to configured rules.
"""

from typing import Optional, Set
from fastapi import HTTPException, UploadFile
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_max_file_size() -> int:
    """
    Get maximum file size from environment variable or use default.

    Returns:
        Maximum file size in bytes
    """
    max_size_mb = os.getenv('MAX_FILE_SIZE_MB', '10')
    try:
        return int(max_size_mb) * 1024 * 1024
    except ValueError:
        return 10 * 1024 * 1024  # Default to 10MB


def get_default_supported_extensions() -> Set[str]:
    """
    Get default supported file extensions.

    Returns:
        Set of supported file extensions
    """
    return {
        '.txt', '.pdf', '.xlsx', '.xls', '.csv', '.html',
        '.htm', '.rtf', '.odt', '.xml', '.json',
        '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'
    }


def is_extension_allowed(file_ext: str) -> bool:
    """
    Check if a file extension is allowed.

    Args:
        file_ext: The file extension to check (with dot, e.g. '.pdf')

    Returns:
        True if the extension is allowed, False otherwise
    """
    # Check if there's an environment variable for allowed extensions
    allowed_extensions_str = os.getenv('ALLOWED_EXTENSIONS')
    if allowed_extensions_str:
        allowed_extensions = {ext.strip().lower() for ext in allowed_extensions_str.split(',')}
        return file_ext.lower() in allowed_extensions
    else:
        # Use default extensions if no environment variable is set
        return file_ext.lower() in get_default_supported_extensions()


def validate_file_for_upload(file: Optional[UploadFile]) -> None:
    """
    Validate an uploaded file according to configured rules.

    Args:
        file: The uploaded file to validate

    Raises:
        HTTPException: If the file fails validation
    """
    if not file:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    # Validate file extension first
    filename = getattr(file, 'filename', '').lower()
    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename provided"
        )

    file_ext = '.' + filename.split('.')[-1] if '.' in filename else ''

    if not is_extension_allowed(file_ext):
        # Get the list of allowed extensions for the error message
        allowed_extensions_str = os.getenv('ALLOWED_EXTENSIONS')
        if allowed_extensions_str:
            allowed_list = allowed_extensions_str
        else:
            allowed_list = ','.join(get_default_supported_extensions())
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file_ext}. Supported types: {allowed_list}"
        )

    # Validate file size
    file_content = file.file.read()
    file_size = len(file_content)

    max_file_size = get_max_file_size()
    if file_size > max_file_size:
        max_size_mb = max_file_size // (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {max_size_mb}MB."
        )

    # Reset file pointer after reading
    file.file.seek(0)


def validate_file_type(filename: str) -> bool:
    """
    Check if a file type is supported.

    Args:
        filename: The name of the file to check

    Returns:
        True if the file type is supported, False otherwise
    """
    if not filename:
        return False

    file_ext = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
    return is_extension_allowed(file_ext)