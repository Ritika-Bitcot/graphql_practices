"""
GraphQL schema definition.

This module combines all GraphQL types, queries, and mutations
into a single schema following the Single Responsibility Principle.
"""

import strawberry
from app.graphql.queries import Query
from app.graphql.mutations import Mutation



# Create the complete schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=strawberry.SchemaConfig(
        auto_camel_case=True,
        validation_enabled=True
    )
)

