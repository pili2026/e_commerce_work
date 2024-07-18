from util.app_error import ServiceException, ErrorCode


def validate_input_length(value: str, min_length: int, max_length: int) -> str:
    if not min_length < len(value) <= max_length:
        raise ServiceException(
            code=ErrorCode.INVALID_FORMAT,
            message=f"The input length must be between {min_length} and {max_length} characters.",
        )
    return value
