"""
Database configuration and session management.

This module provides database connection setup and session management
following the Dependency Inversion Principle.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings


# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_database_session() -> Generator[Session, None, None]:
    """
    Get database session dependency.
    
    This function provides a database session for dependency injection
    following the Dependency Inversion Principle.
    
    Yields:
        Session: Database session object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """
    Create all database tables.
    
    This function creates all tables defined in the models.
    """
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    """
    Drop all database tables.
    
    This function drops all tables defined in the models.
    Use with caution in production environments.
    """
    Base.metadata.drop_all(bind=engine)
