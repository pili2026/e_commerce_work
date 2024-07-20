from typing import Optional
from unittest.mock import AsyncMock, patch
from uuid import UUID, uuid4

import pytest

from service.model.user import User
from service.role_permission import RoleNamesEnum
from service.user import UserService


@pytest.mark.parametrize("user_id_list", [None, [], [uuid4()]])
@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(user_service: UserService, user_id_list: Optional[list[UUID]]):
    # Arrange
    stub_user_list = [
        User(
            id=uuid4(),
            account="manager",
            password="hashed password",
            name="Default Manager",
            role=RoleNamesEnum.MANAGER,
        )
    ]

    with patch.object(
        user_service.user_repository, "get_user_list", AsyncMock(return_value=stub_user_list)
    ) as mock_get_user_list:
        # Act
        result = await user_service.get_user_list(user_id_list)

        # Assert
        assert result == stub_user_list
        mock_get_user_list.assert_called_once_with(user_id_list)
