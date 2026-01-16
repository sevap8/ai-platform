"""
Configuration management for the AI Platform.

This module handles application settings and configuration values.
"""

from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings class.
    
    This class defines all configurable parameters for the application.
    """
    
    # Qdrant Configuration
    qdrant_url: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "documents"
    
    # Application Configuration
    app_name: str = "AI Platform"
    debug: bool = False
    api_prefix: str = "/api/v1"
    
    # Document Processing Configuration
    max_file_size: int = 10 * 1024 * 1024  # 10MB in bytes
    allowed_file_types: list = ["txt", "pdf", "docx", "md"]
    
    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    """
    Get the application settings instance.
    
    Returns:
        Settings instance with loaded configuration values
    """
    return Settings()


# Export the settings instance
settings = get_settings()

__all__ = ["Settings", "get_settings", "settings"]