from functools import wraps
from typing import Annotated, Callable

from fastapi import Depends, HTTPException, Request, status
import jwt

from restful_api.schema.authentication import oauth2_scheme
from service.authentication import AuthenticationService, PayloadField
from service.model.role import RoleNamesEnum
from util.app_error import ErrorCode
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


def check_permissions(required_role: str) -> Callable:
    def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if required_role not in current_user["role"]:
            raise HTTPException(status_code=ErrorCode.INVALID_PERMISSION, detail="Operation not permitted")
        return current_user

    return role_checker


# TODO: Maybe I shouldn't put this here
def check_status_permission(role: str, order_status: str) -> None:
    if role == RoleNamesEnum.CUSTOMER.value and order_status != "Cancel":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Customers can only update the status to 'Cancel'."
        )
