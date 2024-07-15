from enum import Enum


class ErrorCode(Enum):
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_SESSION = "INVALID_SESSION"
    SESSION_EXPIRED = "SESSION_EXPIRED"
    DUPLICATE_ENTRY = "DUPLICATE_ENTRY"
    NOT_FOUND = "NOT_FOUND"
    INVALID_FORMAT = "INVALID_FORMAT"
    SERVER_ERROR = "SERVER_ERROR"

    OUT_OF_STOCK = "OUT_OF_STOCK"
    INSUFFICIENT_STOCK = "INSUFFICIENT_STOCK"


class AppError(Exception):
    def __init__(self, message: str, code: ErrorCode):
        super().__init__(message)
        self.message = message
        self.code = code
