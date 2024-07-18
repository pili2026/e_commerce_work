from enum import IntEnum

from fastapi import HTTPException


class ErrorCode(IntEnum):
    INVALID_CREDENTIALS = 401  # Unauthorized
    INVALID_SESSION = 401  # Unauthorized
    SESSION_EXPIRED = 401  # Unauthorized
    DUPLICATE_ENTRY = 409  # Conflict
    NOT_FOUND = 404  # Not Found
    INVALID_FORMAT = 400  # Bad Request
    SERVER_ERROR = 500  # Internal Server Error

    OUT_OF_STOCK = 400
    INSUFFICIENT_STOCK = 400


class ServiceException(HTTPException):
    def __init__(self, message: str, code: int):
        super().__init__(status_code=code, detail=message)
