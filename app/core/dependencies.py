"""
Dependency injection configuration.

This module provides common dependencies for the application
following the Dependency Inversion Principle.
"""

from typing import Generator
from sqlalchemy.orm import Session

from app.core.database import get_database_session


def get_db() -> Generator[Session, None, None]:
    """
    Get database session dependency.
    
    This is a wrapper around the database session generator
    for consistency in dependency injection.
    
    Yields:
        Session: Database session object
    """
    yield from get_database_session()
