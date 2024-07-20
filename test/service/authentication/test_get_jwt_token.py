import pytest

from service.authentication import AuthenticationService
from util.app_error import ServiceException, ErrorCode


@pytest.mark.asyncio
@pytest.mark.parametrize("authorization_header", ["Bearer<TOKEN>", "Bear<TOKEN>", "<TOKEN>", ""])
async def test_when_authorization_header_does_not_start_with_bearer_then_raise_invalid_format_error(
    authentication_service: AuthenticationService, authorization_header: str
):
    # Act
    with pytest.raises(ServiceException) as error:
        authentication_service.get_jwt_token(authorization_header)

    # Assert
    assert error.value.status_code == ErrorCode.INVALID_FORMAT


@pytest.mark.asyncio
@pytest.mark.parametrize("authorization_header,expected_value", [("Bearer <TOKEN>", "<TOKEN>")])
async def test_when_authorization_header_is_valid_then_return_access_token(
    authentication_service: AuthenticationService,
    authorization_header: str,
    expected_value: str,
):
    # Act
    result = authentication_service.get_jwt_token(authorization_header)

    # Assert
    assert result == expected_value
