from uuid import UUID

import strawberry
from strawberry.types import Info

from graphql_api.decorator.authentication import validate_jwt_token
from graphql_api.schema.authentication import AuthPayload
from service.authentication import AuthenticationService, PayloadField
from service.model.auth_payload import AuthPayload as AuthPayloadModel


@strawberry.type
class AuthenticationMutation:
    @strawberry.mutation
    async def login(self, info: Info, account: str, password: str) -> AuthPayload:
        authentication_service: AuthenticationService = info.context.authentication_service
        auth_payload: AuthPayloadModel = await authentication_service.login(account, password)
        return auth_payload

    @strawberry.mutation
    @validate_jwt_token
    async def logout(self, info: Info) -> None:
        token_payload: dict = info.context.token_payload
        access_token: str = token_payload[PayloadField.SESSION_ID.value]
        authentication_service: AuthenticationService = info.context.authentication_service
        await authentication_service.logout(session_id=UUID(access_token))

    @strawberry.mutation
    async def refresh_token(self, info: Info, refresh_token: str) -> AuthPayload:
        authentication_service: AuthenticationService = info.context.authentication_service
        header_auth = authentication_service.get_header_authorization(info)
        access_token: str = authentication_service.get_jwt_token(header_auth)
        auth_payload: AuthPayloadModel = await authentication_service.refresh_token(access_token, refresh_token)
        return auth_payload
