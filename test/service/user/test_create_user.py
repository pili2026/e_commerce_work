from unittest.mock import AsyncMock, patch

import pytest

from service.authentication import AuthenticationService
from service.model.user import CreateUser, User
from service.role_permission import RoleNamesEnum
from service.user import UserService


@pytest.mark.asyncio
async def test_when_called_then_hash_password_and_delegate_to_repository(user_service: UserService):
    # Arrange
    input_password = "Manager1234"
    stub_hashed_password = "hashed_password"

    user_to_create = CreateUser(
        account="manager",
        password=input_password,
        role=RoleNamesEnum.MANAGER,
    )

    stub_insert_user = User(
        account="manager",
        password=stub_hashed_password,
        role=RoleNamesEnum.MANAGER,
    )

    with (
        patch.object(
            AuthenticationService,
            "hash_password",
            return_value=stub_hashed_password,
        ) as mock_hash_password,
        patch.object(
            user_service.user_repository,
            "insert_user",
            AsyncMock(
                return_value=stub_insert_user,
            ),
        ) as mock_insert_user,
    ):
        # Act
        result = await user_service.create_user(user_to_create)

        # Assert
        assert result == stub_insert_user
        assert user_to_create.password.get_secret_value() == stub_hashed_password

        mock_hash_password.assert_called_once_with(input_password)
        mock_insert_user.assert_called_once_with(user_to_create)
