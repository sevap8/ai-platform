"""
Main application entry point for the AI Platform.

This module initializes the application and sets up all required services.
"""

import os
from dotenv import load_dotenv
from api.routers import app

# Load environment variables from .env file
load_dotenv()


if __name__ == "__main__":
    import uvicorn

    # Run the application with environment variables
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 8000)),
        reload=os.getenv("APP_RELOAD", "true").lower() == "true"
    )