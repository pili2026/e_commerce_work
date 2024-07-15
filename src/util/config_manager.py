import json
import logging

import yaml

from util.app_error import AppError, ErrorCode


log = logging.getLogger(__name__)

__CONFIG_MANAGER = None


class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.__config = None

    def __load_config(self):
        if not self.config_path:
            log.error("The config_path is not provided.")
            return

        with open(file=self.config_path, mode="r", encoding="utf-8") as f:
            self.__config = yaml.safe_load(f)

    def get_config(self) -> dict:
        if not self.__config:
            self.__load_config()

        return self.__config

    def get_readable_config(self) -> str:
        if not self.__config:
            self.__load_config()

        readble_config = json.dumps(self.__config, indent=4, sort_keys=True)
        return readble_config


def set_config_manager(config_manager: ConfigManager):
    global __CONFIG_MANAGER
    __CONFIG_MANAGER = config_manager


def get_config_manager() -> ConfigManager:
    global __CONFIG_MANAGER

    if __CONFIG_MANAGER is None:
        raise AppError(
            message="ConfigManager has not been initialized yet.",
            code=ErrorCode.SERVER_ERROR,
        )

    return __CONFIG_MANAGER
