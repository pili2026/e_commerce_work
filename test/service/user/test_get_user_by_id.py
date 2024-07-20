from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.model.user import User
from service.role_permission import RoleNamesEnum
from service.user import UserService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(user_service: UserService):
    # Arrange
    stub_get_user = User(
        id=uuid4(),
        account="manager",
        password="hashed password",
        name="Default Manager",
        role=RoleNamesEnum.MANAGER,
    )

    with patch.object(user_service.user_repository, "get_user", AsyncMock(return_value=stub_get_user)) as mock_get_user:
        # Act
        result = await user_service.get_user_by_id(stub_get_user.id)

        # Assert
        assert result == stub_get_user
        mock_get_user.assert_called_once_with(user_id=stub_get_user.id)
