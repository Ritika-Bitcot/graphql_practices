"""
GraphQL query resolvers.

This module implements GraphQL query resolvers for the Note entity
following the Single Responsibility Principle.
"""

import logging
from typing import List, Optional
from strawberry import field, type
from sqlalchemy.orm import Session

from app.graphql.types import (
    NoteType,
    NotesResponse,
    NoteResponse,
    StatisticsResponse,
    NotePaginationInput,
    NoteSearchInput,
    NoteStatisticsType
)
from app.services.note_service import NoteService
from app.core.dependencies import get_db

# Configure logging
logger = logging.getLogger(__name__)


class NoteQueryResolver:
    """
    GraphQL query resolver for Note operations.
    
    This class handles all GraphQL queries for notes
    following the Single Responsibility Principle.
    """
    
    def __init__(self, db: Session) -> None:
        """
        Initialize note query resolver.
        
        Args:
            db: Database session
        """
        self.note_service = NoteService.create_from_session(db)
    
    @field
    async def get_note(self, id: int) -> NoteResponse:
        """
        Get a single note by ID.
        
        Args:
            id: ID of the note to retrieve
            
        Returns:
            NoteResponse: Response containing the note or error message
        """
        try:
            note = self.note_service.get_by_id(id)
            
            if note:
                logger.info(f"Retrieved note with ID: {id}")
                return NoteResponse(
                    success=True,
                    message="Note retrieved successfully",
                    note=NoteType(
                        id=note.id,
                        title=note.title,
                        content=note.content,
                        created_at=note.created_at,
                        updated_at=note.updated_at
                    )
                )
            else:
                logger.warning(f"Note not found with ID: {id}")
                return NoteResponse(
                    success=False,
                    message=f"Note with ID {id} not found",
                    note=None
                )
                
        except Exception as e:
            logger.error(f"Error retrieving note with ID {id}: {str(e)}")
            return NoteResponse(
                success=False,
                message=f"Error retrieving note: {str(e)}",
                note=None
            )
    
    @field
    async def get_all_notes(self, pagination: Optional[NotePaginationInput] = None) -> NotesResponse:
        """
        Get all notes with pagination.
        
        Args:
            pagination: Pagination parameters
            
        Returns:
            NotesResponse: Response containing list of notes or error message
        """
        try:
            # Set default pagination if not provided
            if pagination is None:
                pagination = NotePaginationInput()
            
            notes = self.note_service.get_all(
                skip=pagination.skip,
                limit=pagination.limit
            )
            
            # Convert to GraphQL types
            note_types = [
                NoteType(
                    id=note.id,
                    title=note.title,
                    content=note.content,
                    created_at=note.created_at,
                    updated_at=note.updated_at
                )
                for note in notes
            ]
            
            logger.info(f"Retrieved {len(note_types)} notes")
            
            return NotesResponse(
                success=True,
                message="Notes retrieved successfully",
                notes=note_types,
                total=len(note_types)
            )
            
        except ValueError as e:
            logger.error(f"Validation error in get_all_notes: {str(e)}")
            return NotesResponse(
                success=False,
                message=f"Invalid pagination parameters: {str(e)}",
                notes=[],
                total=0
            )
        except Exception as e:
            logger.error(f"Error retrieving notes: {str(e)}")
            return NotesResponse(
                success=False,
                message=f"Error retrieving notes: {str(e)}",
                notes=[],
                total=0
            )
    
    @field
    async def search_notes(self, search_input: NoteSearchInput) -> NotesResponse:
        """
        Search notes by query string.
        
        Args:
            search_input: Search parameters including query and pagination
            
        Returns:
            NotesResponse: Response containing matching notes or error message
        """
        try:
            notes = self.note_service.search(
                query=search_input.query,
                skip=search_input.skip,
                limit=search_input.limit
            )
            
            # Convert to GraphQL types
            note_types = [
                NoteType(
                    id=note.id,
                    title=note.title,
                    content=note.content,
                    created_at=note.created_at,
                    updated_at=note.updated_at
                )
                for note in notes
            ]
            
            logger.info(f"Found {len(note_types)} notes matching query: '{search_input.query}'")
            
            return NotesResponse(
                success=True,
                message=f"Found {len(note_types)} notes matching your search",
                notes=note_types,
                total=len(note_types)
            )
            
        except ValueError as e:
            logger.error(f"Validation error in search_notes: {str(e)}")
            return NotesResponse(
                success=False,
                message=f"Invalid search parameters: {str(e)}",
                notes=[],
                total=0
            )
        except Exception as e:
            logger.error(f"Error searching notes: {str(e)}")
            return NotesResponse(
                success=False,
                message=f"Error searching notes: {str(e)}",
                notes=[],
                total=0
            )
    
    @field
    async def get_note_statistics(self) -> StatisticsResponse:
        """
        Get note statistics.
        
        Returns:
            StatisticsResponse: Response containing statistics or error message
        """
        try:
            stats = self.note_service.get_statistics()
            
            statistics_type = NoteStatisticsType(
                total_notes=stats["total_notes"],
                service_version=stats["service_version"]
            )
            
            logger.info("Retrieved note statistics")
            
            return StatisticsResponse(
                success=True,
                message="Statistics retrieved successfully",
                statistics=statistics_type
            )
            
        except Exception as e:
            logger.error(f"Error retrieving statistics: {str(e)}")
            return StatisticsResponse(
                success=False,
                message=f"Error retrieving statistics: {str(e)}",
                statistics=None
            )


# Create the query schema
@type
class Query:
    """
    GraphQL Query schema.
    
    This class defines all available GraphQL queries
    for the Note entity.
    """
    
@type
class Query:
    """
    GraphQL Query schema.
    
    This class defines all available GraphQL queries
    for the Note entity.
    """

    def __init__(self):
        self.db_gen = get_db()
        self.db = next(self.db_gen)
        self.resolver = NoteQueryResolver(self.db)

    async def close(self):
        try:
            self.db.close()
        finally:
            self.db_gen.close()

    @field
    async def get_note(self, id: int) -> NoteResponse:
        """
        Get a single note by ID.
        
        Args:
            id: ID of the note to retrieve
            
        Returns:
            NoteResponse: Response containing the note or error message
        """
        try:
            return await self.resolver.get_note(id)
        finally:
            await self.close()

    @field
    async def get_all_notes(
        self, 
        pagination: Optional[NotePaginationInput] = None
    ) -> NotesResponse:
        """
        Get all notes with pagination.
        
        Args:
            pagination: Pagination parameters
            
        Returns:
            NotesResponse: Response containing list of notes or error message
        """
        try:
            return await self.resolver.get_all_notes(pagination)
        finally:
            await self.close()

    @field
    async def search_notes(self, search_input: NoteSearchInput) -> NotesResponse:
        """
        Search notes by query string.
        
        Args:
            search_input: Search parameters including query and pagination
            
        Returns:
            NotesResponse: Response containing matching notes or error message
        """
        try:
            return await self.resolver.search_notes(search_input)
        finally:
            await self.close()

    @field
    async def get_note_statistics(self) -> StatisticsResponse:
        """
        Get note statistics.
        
        Returns:
            StatisticsResponse: Response containing statistics or error message
        """
        try:
            return await self.resolver.get_note_statistics()
        finally:
            await self.close()
