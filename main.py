"""
Main application entry point for the AI Platform.

This module initializes the application and sets up all required services.
"""

import asyncio
from api.routers import app
from services.storage_manager import StorageManager


# Global application state
storage_manager = None


@app.on_event("startup")
async def startup_event():
    """
    Initialize services when the application starts.
    """
    global storage_manager
    storage_manager = StorageManager()
    await storage_manager.initialize()


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )