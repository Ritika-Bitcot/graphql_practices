"""
GraphQL schema definition.

This module combines all GraphQL types, queries, and mutations
into a single schema following the Single Responsibility Principle.
"""

import strawberry
from app.graphql.queries import Query
from app.graphql.mutations import Mutation


@strawberry.type
class Schema:
    """
    Root GraphQL schema.
    
    This class combines queries and mutations into a single schema
    for the GraphQL API.
    """
    
    query: Query = strawberry.field(description="Query operations")
    mutation: Mutation = strawberry.field(description="Mutation operations")



# Create and return the complete schema dynamically

def get_schema() -> strawberry.Schema:
    """
    Get the GraphQL schema.
    
    Returns:
        strawberry.Schema: The complete GraphQL schema
    """
    return strawberry.Schema(
        query=Query,
        mutation=Mutation,
        config=strawberry.SchemaConfig(
            auto_camel_case=True,
            validation_enabled=True
        )
    )


def get_schema() -> strawberry.Schema:
    """
    Get the GraphQL schema.
    
    Returns:
        strawberry.Schema: The complete GraphQL schema
    """
    return schema