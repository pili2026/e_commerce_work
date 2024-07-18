from enum import IntEnum

from fastapi import HTTPException


class ErrorCode(IntEnum):
    INVALID_FORMAT = 400
    INVALID_CREDENTIALS = 401
    INVALID_SESSION = 401
    SESSION_EXPIRED = 401
    INVALID_PERMISSION = 403
    NOT_FOUND = 404
    DUPLICATE_ENTRY = 409
    SERVER_ERROR = 500

    OUT_OF_STOCK = 400
    INSUFFICIENT_STOCK = 400


class ServiceException(HTTPException):
    def __init__(self, message: str, code: int):
        super().__init__(status_code=code, detail=message)
