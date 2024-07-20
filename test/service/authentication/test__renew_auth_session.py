# pylint: disable=protected-access, line-too-long

from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from service.authentication import AuthenticationService
from service.model.auth_session import AuthSession, UpdateAuthSession
from util.app_error import ServiceException, ErrorCode


@pytest.mark.asyncio
async def test_when_session_not_found_then_raise_invalid_session_error(
    authentication_service: AuthenticationService,
):
    fake_session_id = UUID("26b20ca7-4622-4445-b20c-a74622644539")
    fake_user_id = UUID("7f5b1fbc-8691-470c-9b1f-bc8691e70c22")
    dummy_expire_at = datetime.strptime("2024-07-02 08:06:12", "%Y-%m-%d %H:%M:%S")

    stub_generated_token = ("<TOKEN>", dummy_expire_at)
    stub_issue_at = datetime.strptime("2024-07-02 08:06:1", "%Y-%m-%d %H:%M:%S")

    # Act
    with (
        patch(
            "service.authentication.get_utc_datetime_now_without_timezone",
            return_value=stub_issue_at,
        ),
        patch.object(
            authentication_service,
            "_create_jwt_token",
            return_value=stub_generated_token,
        ),
        patch.object(
            authentication_service.auth_session_repository,
            "update_auth_session",
            AsyncMock(side_effect=ServiceException(message="", code=ErrorCode.NOT_FOUND)),
        ),
    ):
        with pytest.raises(ServiceException) as error:
            await authentication_service._renew_auth_session(fake_session_id, fake_user_id)

    # Assert
    assert error.value.status_code == ErrorCode.INVALID_SESSION


@pytest.mark.asyncio
async def test_when_arguments_are_valid_then_renew_tokens_and_updated_auth_session(
    authentication_service: AuthenticationService,
):
    fake_session_id = UUID("f3471e23-8dde-4ec7-871e-238ddedec79e")
    fake_user_id = UUID("b2f99edc-0c53-4c1a-b99e-dc0c532c1aa0")
    dummy_expire_at = datetime.strptime("2024-06-28 08:26:22", "%Y-%m-%d %H:%M:%S")

    stub_generated_token = ("<TOKEN>", dummy_expire_at)
    stub_issue_at = datetime.strptime("2024-06-28 08:26:22", "%Y-%m-%d %H:%M:%S")

    stub_auth_session = AuthSession(
        id=fake_session_id,
        user_id=fake_user_id,
        issue_at=stub_issue_at,
        access_token=stub_generated_token[0],
        access_token_expire_at=stub_generated_token[1],
        refresh_token=stub_generated_token[0],
        refresh_token_expire_at=stub_generated_token[1],
    )

    # Act
    with (
        patch.object(
            authentication_service,
            "_create_jwt_token",
            return_value=stub_generated_token,
        ),
        patch.object(
            authentication_service.auth_session_repository,
            "update_auth_session",
            AsyncMock(return_value=stub_auth_session),
        ) as mock_update_auth_session,
        patch(
            "service.authentication.get_utc_datetime_now_without_timezone",
            return_value=stub_issue_at,
        ),
    ):
        result = await authentication_service._renew_auth_session(fake_session_id, fake_user_id)

    # Assert
    expected_auth_session = stub_auth_session
    expected_update_auth_session = UpdateAuthSession(
        issue_at=stub_issue_at,
        access_token=stub_generated_token[0],
        access_token_expire_at=stub_generated_token[1],
        refresh_token=stub_generated_token[0],
        refresh_token_expire_at=stub_generated_token[1],
    )

    assert result == expected_auth_session
    mock_update_auth_session.assert_called_once_with(fake_session_id, expected_update_auth_session)
