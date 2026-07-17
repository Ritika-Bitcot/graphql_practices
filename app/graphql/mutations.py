"""
GraphQL mutation resolvers.

This module implements GraphQL mutation resolvers for the Note entity
following the Single Responsibility Principle.
"""

import logging
from typing import Optional
from strawberry import field, type
from sqlalchemy.orm import Session

from app.graphql.types import (
    NoteType,
    NoteResponse,
    NotesResponse,
    DeleteResponse,
    NoteCreateInput,
    NoteUpdateInput,
    NoteDeleteInput
)
from app.services.note_service import NoteService
from app.core.dependencies import get_db

# Configure logging
logger = logging.getLogger(__name__)


class NoteMutationResolver:
    """
    GraphQL mutation resolver for Note operations.
    
    This class handles all GraphQL mutations for notes
    following the Single Responsibility Principle.
    """
    
    def __init__(self, db: Session) -> None:
        """
        Initialize note mutation resolver.
        
        Args:
            db: Database session
        """
        self.note_service = NoteService.create_from_session(db)
    
    async def create_note(self, note_input: NoteCreateInput) -> NoteResponse:
        """
        Create a new note.
        
        Args:
            note_input: Note creation data
            
        Returns:
            NoteResponse: Response containing created note or error message
        """
        try:
            # Convert input to dictionary
            note_data = {
                "title": note_input.title,
                "content": note_input.content
            }
            
            # Create note using service
            note = self.note_service.create(note_data)
            
            logger.info(f"Created new note with ID: {note.id}")
            
            return NoteResponse(
                success=True,
                message="Note created successfully",
                note=NoteType(
                    id=note.id,
                    title=note.title,
                    content=note.content,
                    created_at=note.created_at,
                    updated_at=note.updated_at
                )
            )
            
        except ValueError as e:
            logger.error(f"Validation error creating note: {str(e)}")
            return NoteResponse(
                success=False,
                message=f"Validation error: {str(e)}",
                note=None
            )
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            return NoteResponse(
                success=False,
                message=f"Error creating note: {str(e)}",
                note=None
            )
    
    async def update_note(self, note_input: NoteUpdateInput) -> NoteResponse:
        """
        Update an existing note.
        
        Args:
            note_input: Note update data
            
        Returns:
            NoteResponse: Response containing updated note or error message
        """
        try:
            # Convert input to dictionary, excluding None values
            update_data = {
                "title": note_input.title,
                "content": note_input.content
            }
            # Remove None values to allow partial updates
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            # Update note using service
            note = self.note_service.update(note_input.id, update_data)
            
            if note:
                logger.info(f"Updated note with ID: {note_input.id}")
                
                return NoteResponse(
                    success=True,
                    message="Note updated successfully",
                    note=NoteType(
                        id=note.id,
                        title=note.title,
                        content=note.content,
                        created_at=note.created_at,
                        updated_at=note.updated_at
                    )
                )
            else:
                logger.warning(f"Note not found for update with ID: {note_input.id}")
                return NoteResponse(
                    success=False,
                    message=f"Note with ID {note_input.id} not found",
                    note=None
                )
                
        except ValueError as e:
            logger.error(f"Validation error updating note: {str(e)}")
            return NoteResponse(
                success=False,
                message=f"Validation error: {str(e)}",
                note=None
            )
        except Exception as e:
            logger.error(f"Error updating note: {str(e)}")
            return NoteResponse(
                success=False,
                message=f"Error updating note: {str(e)}",
                note=None
            )
    
    async def delete_note(self, delete_input: NoteDeleteInput) -> DeleteResponse:
        """
        Delete a note permanently.
        
        Args:
            delete_input: Note deletion data
            
        Returns:
            DeleteResponse: Response containing deletion result or error message
        """
        try:
            # Delete note using service
            success = self.note_service.delete(delete_input.id)
            
            if success:
                logger.info(f"Deleted note with ID: {delete_input.id}")
                
                return DeleteResponse(
                    success=True,
                    message="Note deleted successfully",
                    deleted_id=delete_input.id
                )
            else:
                logger.warning(f"Note not found for deletion with ID: {delete_input.id}")
                
                return DeleteResponse(
                    success=False,
                    message=f"Note with ID {delete_input.id} not found",
                    deleted_id=None
                )
                
        except RuntimeError as e:
            logger.error(f"Runtime error deleting note: {str(e)}")
            return DeleteResponse(
                success=False,
                message=f"Runtime error: {str(e)}",
                deleted_id=None
            )
        except Exception as e:
            logger.error(f"Unhandled error deleting note: {str(e)}")
            return DeleteResponse(
                success=False,
                message="An unexpected error occurred",
                deleted_id=None
            )


# Create the mutation schema
@type
class Mutation:
    """
    GraphQL Mutation schema.
    
    This class defines all available GraphQL mutations
    for the Note entity.
    """
    
    @field
    async def create_note(self, note_input: NoteCreateInput) -> NoteResponse:
        """
        Create a new note.
        
        Args:
            note_input: Note creation data
            
        Returns:
            NoteResponse: Response containing created note or error message
        """
    async def create_note(self, note_input: NoteCreateInput) -> NoteResponse:
        """
        Create a new note.
        
        Args:
            note_input: Note creation data
            
        Returns:
            NoteResponse: Response containing created note or error message
        """
        async with get_db() as db:
            resolver = NoteMutationResolver(db)
            return await resolver.create_note(note_input)
    
    @field
    async def update_note(self, note_input: NoteUpdateInput) -> NoteResponse:
        """
        Update an existing note.
        
        Args:
            note_input: Note update data
            
        Returns:
            NoteResponse: Response containing updated note or error message
        """
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
    async def delete_note(self, delete_input: NoteDeleteInput) -> DeleteResponse:
        """
        Delete a note permanently.
        
        Args:
            delete_input: Note deletion data
            
        Returns:
            DeleteResponse: Response containing deletion result or error message
        """
        async with get_db() as db:
            resolver = NoteMutationResolver(db)
    @field
    async def update_note(self, note_input: NoteUpdateInput) -> NoteResponse:
        """
        Update an existing note.
        
        Args:
            note_input: Note update data
            
        Returns:
            NoteResponse: Response containing updated note or error message
        """
        async with get_db() as db:
            resolver = NoteMutationResolver(db)
            return await resolver.update_note(note_input)