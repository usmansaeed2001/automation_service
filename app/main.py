"""
Main FastAPI application entry point.
Handles router registration, middleware setup, and core application configuration.
"""

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.routers import webhooks

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="Automation Service",
    description="A microservice for handling various automation tasks and integrations",
    version="1.0.0",
)

app.include_router(webhooks.router, prefix="/api/v1", tags=["webhooks"])

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify server status.
    Returns basic service information and status.
    """
    return {"status": "healthy", "service": "automation-service", "version": "1.0.0"}


@app.get("/")
async def root():
    """
    Root endpoint providing basic service information.
    """
    return {"message": "Automation Service API", "version": "1.0.0", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
