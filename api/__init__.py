"""
Main API module for the AI Platform.

This module initializes the API application and handles routing.
"""

from routers import create_app

# Create the main application instance
app = create_app()

# Define the main application object
__all__ = ["app"]