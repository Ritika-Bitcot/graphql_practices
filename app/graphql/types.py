"""
GraphQL type definitions.

This module defines GraphQL types for the Note entity
following the Single Responsibility Principle.
"""

import datetime
from typing import List, Optional
import strawberry


@strawberry.type
class NoteType:
    """
    GraphQL type for Note entity.
    
    This class defines the GraphQL representation of a note
    with proper field definitions and descriptions.
    """
    
    id: int = strawberry.field(description="Unique identifier of the note")
    title: str = strawberry.field(description="Title of the note")
    content: str = strawberry.field(description="Content of the note")
    created_at: datetime.datetime = strawberry.field(description="Timestamp when the note was created")
    updated_at: datetime.datetime = strawberry.field(description="Timestamp when the note was last updated")


@strawberry.input
class NoteCreateInput:
    """
    GraphQL input type for creating a note.
    
    This class defines the input structure for note creation
    with proper validation and descriptions.
    """
    
    title: str = strawberry.field(description="Title of the note")
    content: str = strawberry.field(description="Content of the note")


@strawberry.input
class NoteUpdateInput:
    """
    GraphQL input type for updating a note.
    
    This class defines the input structure for note updates
    with optional fields for partial updates.
    """
    
    id: int = strawberry.field(description="ID of the note to update")
    title: Optional[str] = strawberry.field(
        default=None,
        description="Updated title of the note"
    )
    content: Optional[str] = strawberry.field(
        default=None,
        description="Updated content of the note"
    )


@strawberry.input
class NoteDeleteInput:
    """
    GraphQL input type for deleting a note.
    
    This class defines the input structure for note deletion.
    """
    
    id: int = strawberry.field(description="ID of the note to delete")


@strawberry.input
class NoteSearchInput:
    """
    GraphQL input type for searching notes.
    
    This class defines the input structure for note search
    with pagination support.
    """
    
    query: str = strawberry.field(description="Search query string to match title or content")
    skip: int = strawberry.field(
        default=0,
        description="Number of records to skip for pagination"
    )
    limit: int = strawberry.field(
        default=10,
        description="Maximum number of records to return"
    )


@strawberry.input
class NotePaginationInput:
    """
    GraphQL input type for paginated note queries.
    
    This class defines the input structure for pagination
    with proper validation.
    """
    
    skip: int = strawberry.field(
        default=0,
        description="Number of records to skip for pagination"
    )
    limit: int = strawberry.field(
        default=10,
        description="Maximum number of records to return"
    )


@strawberry.type
class NoteStatisticsType:
    """
    GraphQL type for note statistics.
    
    This class defines the structure for note statistics
    with proper field descriptions.
    """
    
    total_notes: int = strawberry.field(description="Total number of notes")
    service_version: str = strawberry.field(description="Version of the note service")


@strawberry.type
class NoteResponse:
    """
    GraphQL response type for single note operations.
    
    This class defines the response structure for single note
    operations with success/error handling.
    """
    
    success: bool = strawberry.field(description="Indicates if the operation was successful")
    message: str = strawberry.field(description="Response message")
    note: Optional[NoteType] = strawberry.field(description="Note data if successful", default=None)


@strawberry.type
class NotesResponse:
    """
    GraphQL response type for multiple note operations.
    
    This class defines the response structure for multiple note
    operations with pagination support.
    """
    
    success: bool = strawberry.field(description="Indicates if the operation was successful")
    message: str = strawberry.field(description="Response message")
    notes: List[NoteType] = strawberry.field(description="List of notes", default_factory=list)
    total: int = strawberry.field(description="Total number of notes available")


@strawberry.type
class StatisticsResponse:
    """
    GraphQL response type for statistics operations.
    
    This class defines the response structure for statistics
    operations.
    """
    
    success: bool = strawberry.field(description="Indicates if the operation was successful")
    message: str = strawberry.field(description="Response message")
    statistics: Optional[NoteStatisticsType] = strawberry.field(
        description="Statistics data if successful",
        default=None
    )


@strawberry.type
class DeleteResponse:
    """
    GraphQL response type for delete operations.
    
    This class defines the response structure for delete
    operations.
    """
    
    success: bool = strawberry.field(description="Indicates if the operation was successful")
    message: str = strawberry.field(description="Response message")
    deleted_id: Optional[int] = strawberry.field(
        description="ID of the deleted note if successful",
        default=None
    )