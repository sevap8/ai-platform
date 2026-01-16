"""
Main application entry point for the AI Platform.

This module initializes the application and sets up all required services.
"""

import asyncio
from api.routers import app


@app.on_event("startup")
async def startup_event():
    """
    Initialize services when the application starts.
    """
    # The storage manager is initialized in the router module
    pass


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )