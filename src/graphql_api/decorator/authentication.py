from functools import wraps

from service.authentication import AuthenticationService, PayloadField
from util.app_error import AppError, ErrorCode


def validate_jwt_token(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        info = kwargs["info"]
        authentication_service: AuthenticationService = info.context.authentication_service

        header_auth = authentication_service.get_header_authorization(info)
        jwt_token = authentication_service.get_jwt_token(header_auth)
        payload = authentication_service.get_jwt_token_payload(jwt_token)

        session_id = payload[PayloadField.SESSION_ID.value]
        token_exists = await authentication_service.access_token_exists(session_id, jwt_token)

        if not token_exists:
            raise AppError("Token is invalid.", code=ErrorCode.INVALID_SESSION)

        store_token_payload_in_context(info, payload)

        return await func(*args, **kwargs)

    return wrapper


def store_token_payload_in_context(info, token_payload: dict):
    info.context.token_payload = token_payload
