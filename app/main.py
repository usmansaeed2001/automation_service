"""
Main FastAPI application entry point.
Handles router registration, middleware setup, and core application configuration.
"""

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.routers import kajabi_handler
from app.db.db_connection import get_db_manager
import os

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="Automation Service",
    description="A microservice for handling various automation tasks and integrations",
    version="1.0.0",
)

@app.on_event("startup")
async def startup():
    """Initialize database connection on startup"""
    # Initialize database manager with connection string
    db_manager = get_db_manager()
    connection_string = os.getenv('DATABASE_URL')
    if not connection_string:
        raise ValueError("DATABASE_URL environment variable is required")
    db_manager.initialize(connection_string)
    
    # Connect to the database
    db_manager.connect()

@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown"""
    db_manager = get_db_manager()
    db_manager.close()

app.include_router(kajabi_handler.router, prefix="/api/v1", tags=["kajabi-handler"])

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


@app.get("/tables")
async def list_tables():
    """
    List all tables in the database.
    Returns a list of table names and their schemas.
    """
    try:
        # Query to get all tables in the current database
        query = """
        SELECT 
            schemaname,
            tablename,
            tableowner
        FROM pg_tables 
        WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
        ORDER BY schemaname, tablename
        """
        
        db_manager = get_db_manager()
        tables = db_manager.execute_query(query)
        
        # Format the response
        table_list = [
            {
                "schema": table["schemaname"],
                "name": table["tablename"],
                "owner": table["tableowner"]
            }
            for table in tables
        ]
        
        return {
            "tables": table_list,
            "count": len(table_list)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
