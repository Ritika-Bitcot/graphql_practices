"""
Note model for SQLAlchemy.

This module defines the Note entity following the Single
Responsibility Principle for database modeling.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func

from app.core.database import Base


class Note(Base):
    """
    Note model for database representation.
    
    This class represents a note entity in the database
    with proper field definitions and constraints.
    """
    
    __tablename__ = "notes"
    
    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
        nullable=False,
        comment="Unique identifier for the note"
    )
    
    title: str = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Title of the note"
    )
    
    content: str = Column(
        Text,
        nullable=False,
        comment="Content/body of the note"
    )
    
    is_active: bool = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Flag indicating if the note is active"
    )
    
    created_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the note was created"
    )
    
    updated_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Timestamp when the note was last updated"
    )
    
    def __repr__(self) -> str:
        """
        String representation of the Note model.
        
        Returns:
            str: String representation
        """
        return f"Note(id={self.id}, title='{self.title}', is_active={self.is_active})"
    
    def to_dict(self) -> dict:
        """
        Convert note model to dictionary.
        
        Returns:
            dict: Dictionary representation of the note
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at is not None else None,
        }
