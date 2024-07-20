from unittest.mock import MagicMock

import pytest

from service.user import UserService
from repository.user import UserRepository


@pytest.fixture
def user_service() -> UserService:
    return UserService(MagicMock(UserRepository))
