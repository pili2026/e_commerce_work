from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.user import UserService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(user_service: UserService):
    # Arrange
    user_id = uuid4()
    stub_delete_user = True

    with patch.object(
        user_service.user_repository, "delete_user", AsyncMock(return_value=stub_delete_user)
    ) as mock_update_user:
        # Act
        result = await user_service.delete_user(user_id)

        # Assert
        assert result == stub_delete_user
        mock_update_user.assert_called_once_with(user_id)
