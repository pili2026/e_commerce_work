from uuid import UUID
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from restful_api.schema.authentication import AuthPayload as AuthPayloadSchema
from service.authentication import AuthenticationService, PayloadField
from service.model.auth_payload import AuthPayload

from util.authentication import get_current_user
from util.dependency_injector import get_authentication_service

authentication_router = APIRouter()


@authentication_router.post("/login", response_model=AuthPayloadSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authentication_service: AuthenticationService = Depends(get_authentication_service),
):
    auth_payload: AuthPayload = await authentication_service.login(form_data.username, form_data.password)
    return auth_payload


@authentication_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    _: dict = Depends(get_current_user),
    authentication_service: AuthenticationService = Depends(get_authentication_service),
):
    token_payload: dict = request.state.token_payload
    access_token: str = token_payload[PayloadField.SESSION_ID.value]
    await authentication_service.logout(session_id=UUID(access_token))


@authentication_router.post("/refresh-token", response_model=AuthPayloadSchema)
async def refresh_token(
    request: Request,
    refresh_token: str,
    _: dict = Depends(get_current_user),
    authentication_service: AuthenticationService = Depends(get_authentication_service),
):
    header_auth: str = request.headers.get("Authorization")
    access_token: str = authentication_service.get_jwt_token(header_auth)
    auth_payload: AuthPayload = await authentication_service.refresh_token(
        access_token=access_token, refresh_token=refresh_token
    )
    return auth_payload
