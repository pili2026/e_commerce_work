# pylint: disable=line-too-long
from unittest.mock import patch

import pytest

from service.authentication import AuthenticationService
from util.app_error import ServiceException, ErrorCode


@pytest.mark.asyncio
async def test_when_token_is_expired_then_raise_session_expired_error(authentication_service: AuthenticationService):
    # Arrange

    # {
    #     "sub": "4b7e70f2-db53-40fd-be70-f2db5380fded",
    #     "iat": 1719563182,
    #     "exp": 1719566782, (expired time)
    #     "sid": "49364cae-c443-4e9b-b64c-aec443be9bd1"
    #     "role": manager
    #     "permissions": [permission]
    # }
    fake_expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0YjdlNzBmMi1kYjUzLTQwZmQtYmU3MC1mMmRiNTM4MGZkZWQiLCJpYXQiOjE3MTk1NjMxODIsImV4cCI6MTcxOTU2Njc4Miwic2lkIjoiNDkzNjRjYWUtYzQ0My00ZTliLWI2NGMtYWVjNDQzYmU5YmQxIn0.vOv9kcU1ra72A1-9pz9gbdHb3Islt097bxn_L4-eZxg"
    stub_config = {"SECRET_KEY": "73897bec-fd81-44c8-927d-4b3a9773f344", "JWT_ALGORITHM": "HS256"}

    with (
        patch.object(
            authentication_service.config_manager,
            "get_config",
            return_value=stub_config,
        ),
    ):
        # Act
        with pytest.raises(ServiceException) as error:
            authentication_service.get_jwt_token_payload(fake_expired_token)

        # Assert
        assert error.value.status_code == ErrorCode.SESSION_EXPIRED


@pytest.mark.asyncio
async def test_when_token_not_valid_then_raise_invalid_session_error(authentication_service: AuthenticationService):
    # Arrange
    fake_invalid_token = "<JWT_TOKEN>"
    stub_config = {"SECRET_KEY": "73897bec-fd81-44c8-927d-4b3a9773f344", "JWT_ALGORITHM": "HS256"}

    with patch.object(
        authentication_service.config_manager,
        "get_config",
        return_value=stub_config,
    ):
        # Act
        with pytest.raises(ServiceException) as error:
            authentication_service.get_jwt_token_payload(fake_invalid_token)

        # Assert
        assert error.value.status_code == ErrorCode.INVALID_SESSION


@pytest.mark.asyncio
async def test_when_token_is_valid_then_return_token_payload(authentication_service: AuthenticationService):
    # Arrange
    # {
    #     "sub": "4b7e70f2-db53-40fd-be70-f2db5380fded",
    #     "iat": 1719563182,
    #     "exp": 7871243182, (2219-06-07 16:26:22)
    #     "sid": "49364cae-c443-4e9b-b64c-aec443be9bd1"
    # }
    fake_valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0YjdlNzBmMi1kYjUzLTQwZmQtYmU3MC1mMmRiNTM4MGZkZWQiLCJpYXQiOjE3MTk1NjMxODIsImV4cCI6Nzg3MTI0MzE4Miwic2lkIjoiNDkzNjRjYWUtYzQ0My00ZTliLWI2NGMtYWVjNDQzYmU5YmQxIiwicm9sZSI6Im1hbmFnZXIiLCJwZXJtaXNzaW9ucyI6WyJyZWFkX3Byb2R1Y3QiLCJjcmVhdGVfcHJvZHVjdCIsImRlbGV0ZV9wcm9kdWN0IiwidXBkYXRlX3Byb2R1Y3QiLCJyZWFkX2FsbF9vcmRlcnMiXX0.miSMxMrRuMSOPtTojuaJZRl5hlmVMLVFPXvFHQZNjZM"
    stub_config = {"SECRET_KEY": "73897bec-fd81-44c8-927d-4b3a9773f344", "JWT_ALGORITHM": "HS256"}

    with patch.object(
        authentication_service.config_manager,
        "get_config",
        return_value=stub_config,
    ):
        # Act
        result = authentication_service.get_jwt_token_payload(fake_valid_token)

        # Assert
        expected_payload = {
            "sub": "4b7e70f2-db53-40fd-be70-f2db5380fded",
            "iat": 1719563182,
            "exp": 7871243182,
            "sid": "49364cae-c443-4e9b-b64c-aec443be9bd1",
            "role": "manager",
            "permissions": ["read_product", "create_product", "delete_product", "update_product", "read_all_orders"],
        }
        assert result == expected_payload
