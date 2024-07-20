from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from service.authentication import AuthenticationService
from service.model.auth_session import AuthSession
from service.model.role import RoleNamesEnum
from service.model.user import User
from util.app_error import ServiceException, ErrorCode


@pytest.mark.asyncio
async def test_when_user_not_found_then_raise_invalid_credentials_error(
    authentication_service: AuthenticationService,
):
    with (
        patch.object(
            authentication_service.user_repository,
            "get_user",
            AsyncMock(side_effect=ServiceException(message="", code=ErrorCode.NOT_FOUND)),
        ),
    ):
        # Act
        with pytest.raises(ServiceException) as error:
            await authentication_service.login(account="<ACCOUNT>", password="<WRONG_PASSWORD>")

    # Assert
    assert error.value.status_code == ErrorCode.INVALID_CREDENTIALS


@pytest.mark.asyncio
async def test_when_password_is_invalid_then_raise_invalid_credentials_error(
    authentication_service: AuthenticationService,
):
    # Arrange
    stub_user = User(
        account="<ACCOUNT>",
        password="<PASSWORD>",
        name="<NAME>",
        role=RoleNamesEnum.MANAGER,
    )

    with (
        patch.object(
            authentication_service.user_repository,
            "get_user",
            AsyncMock(return_value=stub_user),
        ),
        patch.object(
            authentication_service,
            "_AuthenticationService__is_password_correct",
            return_value=False,
        ),
    ):
        # Act
        with pytest.raises(ServiceException) as error:
            await authentication_service.login(account="<ACCOUNT>", password="<WRONG_PASSWORD>")

        # Assert
        assert error.value.status_code == ErrorCode.INVALID_CREDENTIALS


@pytest.mark.asyncio
async def test_when_password_is_valid_and_create_new_session_then_return_auth_payload(
    authentication_service: AuthenticationService,
):
    # Arrange
    stub_user = User(
        id=UUID("4b7e70f2-db53-40fd-be70-f2db5380fded"),
        account="<ACCOUNT>",
        password="<PASSWORD>",
        name="<NAME>",
        role=RoleNamesEnum.MANAGER,
    )

    dummy_time = datetime.now()
    stub_auth_session = AuthSession(
        id=UUID("49364cae-c443-4e9b-b64c-aec443be9bd1"),
        user_id=stub_user.id,
        issue_at=dummy_time,
        access_token="<ACCESS_TOKEN>",
        access_token_expire_at=dummy_time,
        refresh_token="<REFRESH_TOKEN>",
        refresh_token_expire_at=dummy_time,
    )

    with (
        patch.object(
            authentication_service.user_repository,
            "get_user",
            AsyncMock(return_value=stub_user),
        ),
        patch.object(
            authentication_service,
            "_AuthenticationService__is_password_correct",
            return_value=True,
        ),
        patch.object(
            authentication_service,
            "_create_auth_session",
            AsyncMock(return_value=stub_auth_session),
        ) as mock_create_auth_session,
    ):
        # Act
        result = await authentication_service.login(account="<ACCOUNT>", password="<PASSWORD>")

        # Assert
        assert result.token_type == "Bearer"
        assert result.access_token == stub_auth_session.access_token
        assert result.expires_in == 3600
        assert result.refresh_token == stub_auth_session.refresh_token

        mock_create_auth_session.assert_called_once_with(stub_user)
