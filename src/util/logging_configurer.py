import logging
from enum import Enum

from util.app_error import AppError, ErrorCode


log = logging.getLogger(__name__)


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(level_str: str):
        level_str = level_str.upper()
        if level_str in LogLevel.__members__:
            return LogLevel[level_str]

        raise AppError(
            message=f"Unknown log level: {level_str}",
            code=ErrorCode.SERVER_ERROR,
        )


def configure_logging(log_level_str: str):
    log_level = LogLevel.from_string(log_level_str)
    logging.root.setLevel(level=log_level.value)

    if not logging.root.handlers:
        log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(log_formatter)
        logging.root.addHandler(handler)
