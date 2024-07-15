import strawberry

from graphql_api.resolver.authentication import AuthenticationMutation
from graphql_api.resolver.order import OrderQuery
from graphql_api.resolver.order_detail import OrderDetailMutation, OrderDetailQuery
from graphql_api.resolver.product import ProductMutation, ProductQuery
from graphql_api.resolver.user import UserMutation, UserQuery


@strawberry.type
class RootQuery(UserQuery, ProductQuery, OrderDetailQuery, OrderQuery):
    pass


@strawberry.type
class RootMutation(UserMutation, AuthenticationMutation, ProductMutation, OrderDetailMutation):
    pass
