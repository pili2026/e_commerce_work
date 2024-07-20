# pylint: disable=protected-access, line-too-long

from datetime import datetime, timedelta
from unittest.mock import patch
from uuid import UUID

import pytest

from service.authentication import AuthenticationService
from service.model.permission import PermissionNamesEnum
from service.model.role import RoleNamesEnum


@pytest.mark.asyncio
async def test_when_arguments_are_valid_then_return_access_token_and_expire_at(
    authentication_service: AuthenticationService,
):
    stub_config = {"SECRET_KEY": "73897bec-fd81-44c8-927d-4b3a9773f344", "JWT_ALGORITHM": "HS256"}

    fake_user_id = UUID("4b7e70f2-db53-40fd-be70-f2db5380fded")
    fake_session_id = UUID("49364cae-c443-4e9b-b64c-aec443be9bd1")
    fake_issue_at = datetime.strptime("2024-06-28 08:26:22", "%Y-%m-%d %H:%M:%S")
    fake_life_time = timedelta(hours=1)
    fake_role = RoleNamesEnum.MANAGER
    fake_permissions = [
        PermissionNamesEnum.READ_PRODUCT,
        PermissionNamesEnum.CREATE_PRODUCT,
        PermissionNamesEnum.DELETE_PRODUCT,
        PermissionNamesEnum.UPDATE_PRODUCT,
        PermissionNamesEnum.READ_ALL_ORDERS,
    ]

    # Act
    with patch.object(authentication_service.config_manager, "get_config", return_value=stub_config):
        access_token, expired_at = authentication_service._create_jwt_token(
            user_id=fake_user_id,
            issue_at=fake_issue_at,
            lifetime=fake_life_time,
            session_id=fake_session_id,
            role=fake_role,
            permissions=fake_permissions,
        )

    # Assert
    expected_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0YjdlNzBmMi1kYjUzLTQwZmQtYmU3MC1mMmRiNTM4MGZkZWQiLCJpYXQiOjE3MTk1NjMxODIsImV4cCI6MTcxOTU2Njc4Miwic2lkIjoiNDkzNjRjYWUtYzQ0My00ZTliLWI2NGMtYWVjNDQzYmU5YmQxIiwicm9sZSI6Im1hbmFnZXIiLCJwZXJtaXNzaW9ucyI6WyJyZWFkX3Byb2R1Y3QiLCJjcmVhdGVfcHJvZHVjdCIsImRlbGV0ZV9wcm9kdWN0IiwidXBkYXRlX3Byb2R1Y3QiLCJyZWFkX2FsbF9vcmRlcnMiXX0.L9AZm2KMTVhFSyB27tdTc3Y2iT4dDjRwt7o0INbUhzc"
    expected_expire_at = fake_issue_at + fake_life_time

    assert access_token == expected_access_token
    assert expired_at == expected_expire_at
