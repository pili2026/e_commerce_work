from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from service.authentication import AuthenticationService
from service.model.auth_session import AuthSession
from util.app_error import ErrorCode, ServiceException


@pytest.mark.asyncio
async def test_when_refresh_token_is_expired_then_raise_session_expired_error(
    authentication_service: AuthenticationService,
):
    with patch.object(
        authentication_service,
        "get_jwt_token_payload",
        side_effect=ServiceException(message="", code=ErrorCode.SESSION_EXPIRED),
    ):
        # Act
        with pytest.raises(ServiceException) as error:
            await authentication_service.refresh_token(
                access_token="<USELESS_ACCESS_TOKEN>", refresh_token="<INVALID_REFRESH_TOKEN>"
            )

        # Assert
        assert error.value.status_code == ErrorCode.SESSION_EXPIRED


@pytest.mark.asyncio
async def test_when_refresh_token_is_invalid_then_raise_invalid_session_error(
    authentication_service: AuthenticationService,
):
    with patch.object(
        authentication_service,
        "get_jwt_token_payload",
        side_effect=ServiceException(message="", code=ErrorCode.INVALID_SESSION),
    ):
        # Act
        with pytest.raises(ServiceException) as error:
            await authentication_service.refresh_token(
                access_token="<USELESS_ACCESS_TOKEN>", refresh_token="<INVALID_REFRESH_TOKEN>"
            )

        # Assert
        assert error.value.status_code == ErrorCode.INVALID_SESSION


@pytest.mark.asyncio
async def test_when_session_not_found_then_raise_invalid_session_error(
    authentication_service: AuthenticationService,
):
    # Arrange
    stub_user_id = UUID("52b63647-7044-4e02-b636-4770446e022a")
    stub_auth_session_id = UUID("4925f946-5585-4fbd-a5f9-4655856fbdca")

    stub_refresh_token_payload = {
        "exp": 1721543982,
        "iat": 1718951982,
        "sid": stub_auth_session_id,
        "sub": stub_user_id,
    }

    with (
        patch.object(
            authentication_service,
            "get_jwt_token_payload",
            return_value=stub_refresh_token_payload,
        ),
        patch.object(
            authentication_service.auth_session_repository,
            "get_auth_session",
            AsyncMock(
                side_effect=ServiceException(message="", code=ErrorCode.NOT_FOUND),
            ),
        ),
    ):
        # Act
        with pytest.raises(ServiceException) as error:
            await authentication_service.refresh_token(access_token="<ACCESS_TOKEN>", refresh_token="<REFRESH_TOKEN>")

        # Assert
        assert error.value.status_code == ErrorCode.INVALID_SESSION


@pytest.mark.asyncio
async def test_when_access_token_does_not_match_then_raise_invalid_session_error(
    authentication_service: AuthenticationService,
):
    # Arrange
    stub_user_id = UUID("52b63647-7044-4e02-b636-4770446e022a")

    dummy_time = datetime.now(UTC)
    stub_auth_session = AuthSession(
        id=UUID("4925f946-5585-4fbd-a5f9-4655856fbdca"),
        user_id=stub_user_id,
        issue_at=dummy_time,
        access_token="<DIFFERENT_ACCESS_TOKEN>",
        access_token_expire_at=dummy_time + timedelta(hours=1),
        refresh_token="<REFRESH_TOKEN>",
        refresh_token_expire_at=dummy_time + timedelta(days=90),
    )
    stub_refresh_token_payload = {
        "exp": 1721543982,
        "iat": 1718951982,
        "sid": stub_auth_session.id,
        "sub": stub_user_id,
    }

    with (
        patch.object(
            authentication_service,
            "get_jwt_token_payload",
            return_value=stub_refresh_token_payload,
        ),
        patch.object(
            authentication_service.auth_session_repository,
            "get_auth_session",
            AsyncMock(return_value=stub_auth_session),
        ),
    ):
        # Act
        with pytest.raises(ServiceException) as error:
            await authentication_service.refresh_token(access_token="<ACCESS_TOKEN>", refresh_token="<REFRESH_TOKEN>")

        # Assert
        assert error.value.status_code == ErrorCode.INVALID_SESSION


@pytest.mark.asyncio
async def test_when_refresh_token_valid_then_renew_auth_session_and_return_auth_payload(
    authentication_service: AuthenticationService,
):
    # Arrange
    stub_user_id = UUID("9c5b9669-269e-4f97-9b96-69269ecf97f7")

    dummy_time = datetime.now()
    stub_auth_session = AuthSession(
        id=UUID("49364cae-c443-4e9b-b64c-aec443be9bd1"),
        user_id=stub_user_id,
        issue_at=dummy_time,
        access_token="<ACCESS_TOKEN>",
        access_token_expire_at=dummy_time,
        refresh_token="<REFRESH_TOKEN>",
        refresh_token_expire_at=dummy_time,
    )

    stub_refresh_token_payload = {
        "exp": 1721543982,
        "iat": 1718951982,
        "sid": stub_auth_session.id,
        "sub": stub_user_id,
    }

    with (
        patch.object(
            authentication_service,
            "get_jwt_token_payload",
            return_value=stub_refresh_token_payload,
        ) as mock_get_jwt_token_payload,
        patch.object(
            authentication_service.auth_session_repository,
            "get_auth_session",
            AsyncMock(return_value=stub_auth_session),
        ) as mock_get_auth_session,
        patch.object(
            authentication_service,
            "_renew_auth_session",
            AsyncMock(return_value=stub_auth_session),
        ) as mock_renew_auth_session,
    ):
        # Act
        result = await authentication_service.refresh_token(
            access_token=stub_auth_session.access_token, refresh_token=stub_auth_session.refresh_token
        )

        # Assert
        assert result.token_type == "Bearer"
        assert result.access_token == stub_auth_session.access_token
        assert result.expires_in == 3600
        assert result.refresh_token == stub_auth_session.refresh_token

        mock_get_jwt_token_payload.assert_called_once_with(stub_auth_session.refresh_token)
        mock_get_auth_session.assert_called_once_with(stub_auth_session.id)
        mock_renew_auth_session.assert_called_once_with(stub_auth_session.id, stub_user_id)
