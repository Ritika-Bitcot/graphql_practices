"""
Pydantic schemas for Note entity.

This module defines request/response schemas for the Note entity
following the Single Responsibility Principle for validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class NoteBase(BaseModel):
    """
    Base schema for Note entity.
    
    This class contains common fields for note schemas.
    """
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Title of the note"
    )
    
    content: str = Field(
        ...,
        min_length=1,
        description="Content of the note"
    )
    
    @validator('title')
    def validate_title(cls, v: str) -> str:
        """
        Validate title field.
        
        Args:
            v: Title value
            
        Returns:
            str: Validated title
            
        Raises:
            ValueError: If title is invalid
        """
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()
    
    @validator('content')
    def validate_content(cls, v: str) -> str:
        """
        Validate content field.
        
        Args:
            v: Content value
            
        Returns:
            str: Validated content
            
        Raises:
            ValueError: If content is invalid
        """
        if not v.strip():
            raise ValueError("Content cannot be empty or whitespace")
        return v.strip()


class NoteCreate(NoteBase):
    """
    Schema for creating a new note.
    
    This class is used for note creation requests.
    """
    
    pass


class NoteUpdate(BaseModel):
    """
    Schema for updating an existing note.
    
    This class is used for note update requests.
    All fields are optional to allow partial updates.
    """
    
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated title of the note"
    )
    
    content: Optional[str] = Field(
        None,
        min_length=1,
        description="Updated content of the note"
    )
    
    @validator('title')
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate title field for updates.
        
        Args:
            v: Title value
            
        Returns:
            Optional[str]: Validated title or None
        """
        if v is None:
            return None
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()
    
    @validator('content')
    def validate_content(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate content field for updates.
        
        Args:
            v: Content value
            
        Returns:
            Optional[str]: Validated content or None
        """
        if v is None:
            return None
        if not v.strip():
            raise ValueError("Content cannot be empty or whitespace")
        return v.strip()


class NoteResponse(NoteBase):
    """
    Schema for note response.
    
    This class is used for note response data.
    """
    
    id: int = Field(..., description="Unique identifier of the note")
    created_at: datetime = Field(..., description="Timestamp when the note was created")
    updated_at: datetime = Field(..., description="Timestamp when the note was last updated")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
