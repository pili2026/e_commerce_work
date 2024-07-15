import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

from graphql_api.context import get_context
from graphql_api.extension.api_error_handler import APIErrorHandler
from graphql_api.resolver_registry import RootMutation, RootQuery


graphql_schema = strawberry.Schema(
    query=RootQuery,
    mutation=RootMutation,
    config=StrawberryConfig(auto_camel_case=True),
    extensions=[APIErrorHandler],
)
graphql_router = GraphQLRouter(
    graphql_schema,
    context_getter=get_context,
)
