from unittest.mock import MagicMock

import pytest

from repository.auth_session import AuthSessionRepository
from repository.user import UserRepository
from service.authentication import AuthenticationService
from util.config_manager import ConfigManager


@pytest.fixture()
def authentication_service() -> AuthenticationService:
    return AuthenticationService(MagicMock(AuthSessionRepository), MagicMock(UserRepository), MagicMock(ConfigManager))
