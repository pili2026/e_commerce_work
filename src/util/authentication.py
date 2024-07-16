from functools import wraps
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
import jwt

from restful_api.schema.authentication import oauth2_scheme
from service.authentication import AuthenticationService, PayloadField
from util.app_error import AppError, ErrorCode
from util.dependency_injector import get_authentication_service


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
    authentication_service: AuthenticationService = Depends(get_authentication_service),
):
    try:
        payload: dict = authentication_service.get_jwt_token_payload(token)
        session_id: str = payload.get(PayloadField.SESSION_ID.value)
        if not session_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_exists = await authentication_service.access_token_exists(session_id, token)
        if not token_exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        request.state.token_payload = payload
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
