# pylint: disable=protected-access

from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from service.authentication import AuthenticationService
from service.model.auth_session import AuthSession
from service.model.permission import PermissionNamesEnum
from service.model.role import RoleNamesEnum
from service.model.role_permission import RolePermission
from service.model.user import User


@pytest.mark.asyncio
async def test_when_arguments_are_valid_then_generate_tokens_and_create_auth_session(
    authentication_service: AuthenticationService,
):

    dummy_expire_at = datetime.strptime("2024-06-28 08:26:22", "%Y-%m-%d %H:%M:%S")

    stub_generated_token = ("<TOKEN>", dummy_expire_at)
    stub_session_id = UUID("f3471e23-8dde-4ec7-871e-238ddedec79e")
    stub_issue_at = datetime.strptime("2024-06-28 08:26:22", "%Y-%m-%d %H:%M:%S")

    stub_user = User(
        id=UUID("b2f99edc-0c53-4c1a-b99e-dc0c532c1aa0"),
        account="manager",
        password="Manager1234",
        role=RoleNamesEnum.MANAGER,
        role_permission_list=[
            RolePermission(
                role=RoleNamesEnum.MANAGER,
                permission=PermissionNamesEnum.CREATE_PRODUCT,
            ),
            RolePermission(
                role=RoleNamesEnum.MANAGER,
                permission=PermissionNamesEnum.READ_PRODUCT,
            ),
            RolePermission(
                role=RoleNamesEnum.MANAGER,
                permission=PermissionNamesEnum.UPDATE_PRODUCT,
            ),
            RolePermission(
                role=RoleNamesEnum.MANAGER,
                permission=PermissionNamesEnum.DELETE_PRODUCT,
            ),
            RolePermission(
                role=RoleNamesEnum.MANAGER,
                permission=PermissionNamesEnum.READ_ALL_ORDERS,
            ),
        ],
    )

    stub_auth_session = AuthSession(
        id=stub_session_id,
        user_id=stub_user.id,
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
            "insert_auth_session",
            AsyncMock(return_value=stub_auth_session),
        ) as mock_insert_auth_session,
        patch(
            "service.authentication.get_utc_datetime_now_without_timezone",
            return_value=stub_issue_at,
        ),
        patch(
            "service.authentication.uuid4",
            return_value=stub_session_id,
        ),
    ):
        result = await authentication_service._create_auth_session(stub_user)

    # Assert
    expected_auth_session = stub_auth_session
    assert result == expected_auth_session
    mock_insert_auth_session.assert_called_once_with(expected_auth_session)
