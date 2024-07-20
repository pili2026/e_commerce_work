from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from service.authentication import AuthenticationService
from service.model.auth_session import AuthSession
from util.app_error import ServiceException, ErrorCode


@pytest.mark.asyncio
async def test_when_session_does_not_exist_then_return_false(authentication_service: AuthenticationService):
    # Arrange
    with patch.object(
        authentication_service.auth_session_repository,
        "get_auth_session",
        AsyncMock(side_effect=ServiceException(message="", code=ErrorCode.NOT_FOUND)),
    ):
        # Act
        result = await authentication_service.access_token_exists(
            session_id=UUID("4ec7360f-978a-498e-8736-0f978a898e37"), access_token="<ACCESS_TOKEN>"
        )

        # Assert
        assert result is False


@pytest.mark.asyncio
async def test_when_access_token_does_not_match_then_return_false(authentication_service: AuthenticationService):
    # Arrange
    fake_input_access_token = "<ACCESS_TOKEN>"
    stub_access_token = "<DIFFERENT_ACCESS_TOKEN>"

    stub_now = datetime.now(UTC)
    stub_auth_session = AuthSession(
        id=UUID("0702a674-f34e-4622-82a6-74f34e6622ae"),
        user_id=UUID("0b1c1007-9480-4083-9c10-079480e08386"),
        issue_at=stub_now,
        access_token=stub_access_token,
        access_token_expire_at=stub_now + timedelta(hours=1),
        refresh_token="<REFRESH_TOKEN>",
        refresh_token_expire_at=stub_now + timedelta(days=90),
    )
    with patch.object(
        authentication_service.auth_session_repository, "get_auth_session", AsyncMock(return_value=stub_auth_session)
    ) as mock_get_auth_session:
        # Act
        result = await authentication_service.access_token_exists(
            session_id=stub_auth_session.id, access_token=fake_input_access_token
        )

        # Assert
        assert result is False
        mock_get_auth_session.assert_called_once_with(stub_auth_session.id)


@pytest.mark.asyncio
async def test_when_access_token_exists_then_return_true(authentication_service: AuthenticationService):
    # Arrange
    stub_now = datetime.now(UTC)
    stub_auth_session = AuthSession(
        id=UUID("0702a674-f34e-4622-82a6-74f34e6622ae"),
        user_id=UUID("0b1c1007-9480-4083-9c10-079480e08386"),
        issue_at=stub_now,
        access_token="<ACCESS_TOKEN>",
        access_token_expire_at=stub_now + timedelta(hours=1),
        refresh_token="<REFRESH_TOKEN>",
        refresh_token_expire_at=stub_now + timedelta(days=90),
    )
    with patch.object(
        authentication_service.auth_session_repository, "get_auth_session", AsyncMock(return_value=stub_auth_session)
    ) as mock_get_auth_session:
        # Act
        result = await authentication_service.access_token_exists(
            session_id=stub_auth_session.id, access_token="<ACCESS_TOKEN>"
        )

        # Assert
        assert result is True
        mock_get_auth_session.assert_called_once_with(stub_auth_session.id)
