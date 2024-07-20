import uuid
from unittest.mock import AsyncMock, patch

import pytest

from service.authentication import AuthenticationService


@pytest.mark.asyncio
async def test_when_logout_succeeds_and_delete_auth_session_then_return_bool(
    authentication_service: AuthenticationService,
):
    # Arrange
    with patch.object(
        authentication_service.auth_session_repository, "delete_auth_session", AsyncMock(return_value=True)
    ) as mock_delete_auth_session:
        # Act
        session_id = uuid.uuid4()
        result = await authentication_service.logout(session_id=session_id)

        # Assert
        assert result is True
        mock_delete_auth_session.assert_called_once_with(session_id)
