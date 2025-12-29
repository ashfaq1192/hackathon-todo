"""
Main FastAPI application entry point.

This module creates the FastAPI app instance, registers exception handlers,
and includes all API routes.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from src.core.errors import (
    AuthError,
    DatabaseError,
    ForbiddenError,
    NotFoundError,
    auth_error_handler,
    database_error_handler,
    forbidden_error_handler,
    general_exception_handler,
    http_exception_handler,
    not_found_error_handler,
)
from src.database import init_db, get_engine
# Import models to register them with SQLModel.metadata before table creation
from src.models import Task  # noqa: F401

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.

    Handles startup and shutdown events:
    - Startup: Initialize database tables
    - Shutdown: Cleanup resources

    Args:
        app: The FastAPI application instance
    """
    # Startup
    import os

    # Skip database initialization during tests (test fixtures handle it)
    if os.environ.get("PYTEST_IN_PROGRESS") != "1":
        logger.info("Starting up FastAPI application...")
        try:
            engine = get_engine()
            init_db(engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    else:
        logger.info("Test mode: skipping app startup database initialization")

    yield

    # Shutdown
    if os.environ.get("PYTEST_IN_PROGRESS") != "1":
        logger.info("Shutting down FastAPI application...")


# Create FastAPI application instance
app = FastAPI(
    title="Todo API",
    description="RESTful API for Todo CRUD Operations (Phase II - Stage 2)",
    version="0.2.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS middleware to allow frontend requests
import os

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, PATCH, DELETE, OPTIONS)
    allow_headers=["*"],  # Allow all headers
)


# Register Exception Handlers (T037-T040)

# Custom exception handlers
app.add_exception_handler(AuthError, auth_error_handler)
app.add_exception_handler(ForbiddenError, forbidden_error_handler)
app.add_exception_handler(NotFoundError, not_found_error_handler)

# HTTP exception handler
app.add_exception_handler(HTTPException, http_exception_handler)

# Database error handler
app.add_exception_handler(SQLAlchemyError, database_error_handler)
app.add_exception_handler(DatabaseError, database_error_handler)

# General exception handler (catch-all)
app.add_exception_handler(Exception, general_exception_handler)


# Health Check Endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        Simple status response indicating the API is running

    Example response:
        {
            "status": "healthy",
            "service": "Todo API",
            "version": "0.2.0"
        }
    """
    return {
        "status": "healthy",
        "service": "Todo API",
        "version": "0.2.0",
    }


# Root Endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.

    Returns:
        Welcome message and links to documentation

    Example response:
        {
            "message": "Welcome to Todo API",
            "docs": "/docs",
            "health": "/health"
        }
    """
    return {
        "message": "Welcome to Todo API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }


# Temporary Migration Endpoint (DELETE AFTER USE)
@app.post("/migrate/fix-priority-enum", tags=["Migration"])
async def run_priority_enum_migration():
    """
    TEMPORARY: Run priority enum case fix migration.

    This endpoint will be removed after the migration is complete.
    DELETE THIS ENDPOINT after successful migration!
    """
    try:
        from sqlalchemy import text
        from src.database import get_engine

        engine = get_engine()
        results = []

        with engine.connect() as conn:
            # Step 1: Convert to VARCHAR
            conn.execute(text("ALTER TABLE tasks ALTER COLUMN priority TYPE VARCHAR(10);"))
            conn.commit()
            results.append("✓ Converted to VARCHAR")

            # Step 2: Update values to lowercase
            result = conn.execute(text("""
                UPDATE tasks SET priority = LOWER(priority)
                WHERE priority IN ('LOW', 'MEDIUM', 'HIGH');
            """))
            conn.commit()
            results.append(f"✓ Updated {result.rowcount} rows to lowercase")

            # Step 3: Drop old ENUM
            conn.execute(text("DROP TYPE IF EXISTS taskpriority CASCADE;"))
            conn.commit()
            results.append("✓ Dropped old ENUM type")

            # Step 4: Create new ENUM
            conn.execute(text("CREATE TYPE taskpriority AS ENUM ('low', 'medium', 'high');"))
            conn.commit()
            results.append("✓ Created new ENUM type")

            # Step 5: Drop default
            conn.execute(text("ALTER TABLE tasks ALTER COLUMN priority DROP DEFAULT;"))
            conn.commit()
            results.append("✓ Dropped default constraint")

            # Step 6: Convert back to ENUM
            conn.execute(text("""
                ALTER TABLE tasks ALTER COLUMN priority TYPE taskpriority
                USING priority::taskpriority;
            """))
            conn.commit()
            results.append("✓ Converted back to ENUM")

            # Step 7: Restore default
            conn.execute(text("ALTER TABLE tasks ALTER COLUMN priority SET DEFAULT 'medium'::taskpriority;"))
            conn.commit()
            results.append("✓ Restored default value")

        return {
            "status": "success",
            "message": "Migration completed successfully!",
            "steps": results
        }

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


# Register API Routes (T054)
from src.api.routes.tasks import router as tasks_router

app.include_router(tasks_router, prefix="/api", tags=["Tasks"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
