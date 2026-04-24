"""
Note repository implementation.

This module implements the repository pattern for Note entity
following the Single Responsibility and Dependency Inversion principles.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.note import Note


class BaseRepository(ABC):
    """
    Abstract base repository class.
    
    This class defines the interface for all repositories
    following the Dependency Inversion Principle.
    """
    
    @abstractmethod
    def create(self, **kwargs) -> Note:
        """Create a new entity."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[Note]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Note]:
        """Get all entities with pagination."""
        pass
    
    @abstractmethod
    def update(self, entity_id: int, **kwargs) -> Optional[Note]:
        """Update an entity."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an entity."""
        pass


class NoteRepository(BaseRepository):
    """
    Repository implementation for Note entity.
    
    This class handles all database operations for notes
    following the Single Responsibility Principle.
    """
    
    def __init__(self, db: Session) -> None:
        """
        Initialize note repository.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def create(self, title: str, content: str, is_active: bool = True) -> Note:
        """
        Create a new note.
        
        Args:
            title: Title of the note
            content: Content of the note
            is_active: Active status of the note
            
        Returns:
            Note: Created note entity
        """
        note = Note(
            title=title,
            content=content,
            is_active=is_active
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note
    
    def get_by_id(self, entity_id: int) -> Optional[Note]:
        """
        Get note by ID.
        
        Args:
            entity_id: ID of the note
            
        Returns:
            Optional[Note]: Note entity if found, None otherwise
        """
        return self.db.query(Note).filter(Note.id == entity_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Note]:
        """
        Get all notes with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Note]: List of note entities
        """
        return self.db.query(Note).offset(skip).limit(limit).all()
    
    def search(self, query_str: str, skip: int = 0, limit: int = 100) -> List[Note]:
        """
        Search notes by title or content.
        
        Args:
            query_str: Search query string
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Note]: List of matching note entities
        """
        search_filter = or_(
            Note.title.ilike(f"%{query_str}%"),
            Note.content.ilike(f"%{query_str}%")
        )
        
        return (
            self.db.query(Note)
            .filter(search_filter)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update(self, entity_id: int, **kwargs) -> Optional[Note]:
        """
        Update a note.
        
        Args:
            entity_id: ID of the note to update
            **kwargs: Fields to update
            
        Returns:
            Optional[Note]: Updated note entity if found, None otherwise
        """
        note = self.get_by_id(entity_id)
        if not note:
            return None
        
        for key, value in kwargs.items():
            if hasattr(note, key) and value is not None:
                setattr(note, key, value)
        
        self.db.commit()
        self.db.refresh(note)
        return note
    
    def delete(self, entity_id: int) -> bool:
        """
        Delete a note permanently from database.
        
        Args:
            entity_id: ID of the note to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        note = self.get_by_id(entity_id)
        if not note:
            return False
        
        self.db.delete(note)
        self.db.commit()
        return True
    
    def count(self) -> int:
        """
        Count notes.
        
        Returns:
            int: Number of notes
        """
        return self.db.query(Note).count()
