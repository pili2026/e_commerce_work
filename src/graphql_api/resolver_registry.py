import strawberry

from graphql_api.resolver.authentication import AuthenticationMutation
from graphql_api.resolver.user import UserMutation, UserQuery


@strawberry.type
class RootQuery(UserQuery):
    pass


@strawberry.type
class RootMutation(UserMutation, AuthenticationMutation):
    pass
