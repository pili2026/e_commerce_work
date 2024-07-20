from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.model.user import UpdateUser, User
from service.role_permission import RoleNamesEnum
from service.user import UserService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(user_service: UserService):
    # Arrange
    user_id = uuid4()
    user_to_update = UpdateUser(
        name="Default Manager",
        role=RoleNamesEnum.MANAGER,
    )

    stub_update_user = User(
        id=user_id,
        account="namager",
        password="hashed_password",
        name="Default Manager",
        role=RoleNamesEnum.MANAGER,
    )

    with patch.object(
        user_service.user_repository, "update_user", AsyncMock(return_value=stub_update_user)
    ) as mock_update_user:
        # Act
        result = await user_service.update_user(user_id, user_to_update)

        # Assert
        assert result == stub_update_user
        mock_update_user.assert_called_once_with(user_id, user_to_update)
