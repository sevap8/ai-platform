"""
Services module for the AI Platform.

This module contains business logic services that coordinate between
different components of the application.
"""

from .storage_manager import StorageManager

__all__ = ["StorageManager"]