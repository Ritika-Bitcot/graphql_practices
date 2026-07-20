"""
Note service layer.

This module implements business logic for Note operations
following the Single Responsibility Principle.
"""

import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.models.note import Note

# Configure logging
logger = logging.getLogger(__name__)


class NoteService:
    """
    Service class for Note business logic.
    
    This class handles all business operations for notes
    following the Single Responsibility Principle.
    """
    
    def __init__(self, db: Session) -> None:
        """
        Initialize note service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    @classmethod
    def _validate_pagination_params(cls, skip: int, limit: int) -> None:
        """
        Validate pagination parameters for skip and limit.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
        
        Raises:
            ValueError: If parameters are invalid
        """
        if skip < 0:
            raise ValueError("Skip parameter must be non-negative")
        if limit < 1 or limit > 100:
            raise ValueError("Limit parameter must be between 1 and 100")
    def get_by_id(self, note_id: int) -> Optional[Note]:
        """
        Get a note by ID.
        
        Args:
            note_id: ID of the note to retrieve
            
        Returns:
            Optional[Note]: Note object if found, None otherwise
        """
        try:
            return self.db.query(Note).filter(
                Note.id == note_id,
                Note.is_active == True
            ).first()
        except Exception as e:
            logger.error(f"Error getting note by ID {note_id}: {str(e)}")
            raise
    
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Note]:
        """
        Get all notes with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Note]: List of notes
            self._validate_pagination_params(skip, limit)
        """
        try:
            if skip < 0:
                raise ValueError("Skip parameter must be non-negative")
            if limit < 1 or limit > 100:
                raise ValueError("Limit parameter must be between 1 and 100")
            
            return self.db.query(Note).filter(
                Note.is_active == True
            ).offset(skip).limit(limit).all()
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error getting all notes: {str(e)}")
            raise
    def search(self, query: str, skip: int = 0, limit: int = 10) -> List[Note]:
        """
        Search notes by query string.
        
        Args:
            query: Search query string
            skip: Number of records to skip
            limit: Maximum number of records to return
        
        Returns:
            List[Note]: List of matching notes
        
        Raises:
            ValueError: If search parameters are invalid
        """
        try:
            if not query or not query.strip():
                raise ValueError("Search query cannot be empty")
            self._validate_pagination_params(skip, limit)
            search_term = f"%{query.strip()}%"
            
            return self.db.query(Note).filter(
                Note.is_active == True,
                or_(
                    Note.title.ilike(search_term),
                    Note.content.ilike(search_term)
                )
            ).offset(skip).limit(limit).all()
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error searching notes: {str(e)}")
            raise
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get note statistics.
        
        Returns:
            Dict[str, Any]: Statistics dictionary
        """
        try:
            total_notes = self.db.query(func.count(Note.id)).filter(
                Note.is_active == True
            ).scalar()
            
            return {
                "total_notes": total_notes,
                "service_version": "1.0.0"
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            raise
    
    def create(self, title: str, content: str) -> Note:
        """
        Create a new note.
        
        Args:
            title: Title of the note
            content: Content of the note
            
        Returns:
            Note: Created note object
        """
        try:
            note = Note(
                title=title.strip(),
                content=content.strip()
            )
            
            self.db.add(note)
            self.db.commit()
            self.db.refresh(note)
            
            logger.info(f"Created note with ID: {note.id}")
            return note
            
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            self.db.rollback()
            raise
    
    def update(self, note_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Note]:
        """
        Update an existing note.
        
        Args:
            note_id: ID of the note to update
            title: New title (optional)
            content: New content (optional)
            
        Returns:
            Optional[Note]: Updated note object if found, None otherwise
        """
        try:
            note = self.get_by_id(note_id)
            
            if not note:
                return None
            
            if title is not None:
                note.title = title.strip()
            if content is not None:
                note.content = content.strip()
            
            self.db.commit()
            self.db.refresh(note)
            
            logger.info(f"Updated note with ID: {note_id}")
            return note
            
        except Exception as e:
            logger.error(f"Error updating note {note_id}: {str(e)}")
            self.db.rollback()
            raise
    
    def delete(self, note_id: int) -> bool:
        """
        Soft delete a note (mark as inactive).
        
        Args:
            note_id: ID of the note to delete
            
        Returns:
            bool: True if note was deleted, False if not found
        """
        try:
            note = self.get_by_id(note_id)
            
            if not note:
                return False
            
            note.is_active = False
            self.db.commit()
            
            logger.info(f"Deleted note with ID: {note_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting note {note_id}: {str(e)}")
            self.db.rollback()
            raise