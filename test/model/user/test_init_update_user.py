import pytest
from pydantic import ValidationError

from service.model.user import RoleNamesEnum, UpdateUser


@pytest.mark.parametrize("name", ["", "a" * 20])
def test_when_name_length_valid_then_no_error_raised(name):
    # Act
    user = UpdateUser(name=name, role=RoleNamesEnum.CUSTOMER)

    # Assert
    assert user


@pytest.mark.parametrize("name", ["a" * 21])
def test_when_name_length_invalid_then_raise_validation_error(name):
    # Act
    with pytest.raises(ValidationError) as exc_info:
        UpdateUser(name=name, role=RoleNamesEnum.CUSTOMER)

    # Assert
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == "name"


def test_when_optional_name_missing_then_no_error_raised():
    # Act
    user = UpdateUser(role=RoleNamesEnum.MANAGER)

    # Assert
    assert user
