"""
FastAPI main application.

This module creates and configures the FastAPI application
with GraphQL support following SOLID principles.
"""

import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import strawberry

from app.core.config import settings
from app.core.database import create_tables
from app.graphql.schema import get_schema

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """
    Application lifespan manager.
    
    This function handles startup and shutdown events
    following the Single Responsibility Principle.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info("Starting Notes GraphQL API...")
    
    try:
        # Create database tables
        create_tables()
        logger.info("Database tables created successfully")
        
        # Log application info
        logger.info(f"Application: {settings.app_name} v{settings.app_version}")
        logger.info(f"Debug mode: {settings.debug}")
        logger.info(f"GraphQL debug: {settings.graphql_debug}")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Notes GraphQL API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A FastAPI application implementing CRUD operations for notes using GraphQL and PostgreSQL",
    debug=settings.debug,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trusteddomain.com"],  # Restrict to trusted domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create GraphQL router
def create_graphql_app() -> GraphQLRouter:
    """
    Create GraphQL application with custom context.
    
    Returns:
        GraphQLRouter: Configured GraphQL router
    """
    # Get GraphQL schema
    schema = get_schema()
    
    # Create GraphQL router
    graphql_app = GraphQLRouter(
        schema,
        graphiql=settings.graphql_debug,
        debug=settings.graphql_debug
    )
    
    return graphql_app


# Add GraphQL router
graphql_router = create_graphql_app()
app.include_router(graphql_router, prefix="/graphql")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        Dict[str, Any]: Health status information
    """
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> Dict[str, Any]:
    """
    Root endpoint with basic information.
    
    Returns:
        Dict[str, Any]: Application information
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "graphql_endpoint": "/graphql",
        "health_check": "/health",
        "documentation": {
            "graphql": "/graphql" if settings.graphql_debug else "GraphQL IDE disabled in production"
        }
    }


# Custom middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    """
    Log HTTP requests and responses.
    
    Args:
        request: Incoming HTTP request
        call_next: Next middleware in chain
        
    Returns:
        Response: HTTP response
    """
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    logger.info(f"Response: {response.status_code}")
    
    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> Dict[str, Any]:
    """
    Global exception handler.
    
    Args:
        request: HTTP request
        exc: Exception that occurred
        
    Returns:
        Dict[str, Any]: Error response
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "type": type(exc).__name__ if settings.debug else None
        }
    )


# Run the application
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )
