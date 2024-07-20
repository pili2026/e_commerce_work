from uuid import uuid4

import pytest
from pydantic import ValidationError

from service.model.user import CreateUser, RoleNamesEnum


@pytest.mark.parametrize("account", ["a", "a" * 20])
def test_when_account_length_valid_then_no_error_raised(account):
    # Act
    user = CreateUser(
        id=uuid4(), account=account, password="valid_password", name="Test User", role=RoleNamesEnum.MANAGER
    )

    # Assert
    assert user


@pytest.mark.parametrize("account", [None, "", "a" * 21])
def test_when_account_length_invalid_then_raise_validation_error(account):
    # Act
    with pytest.raises(ValidationError) as exc_info:
        CreateUser(id=uuid4(), account=account, password="valid_password", name="Test User", role=RoleNamesEnum.MANAGER)

    # Assert
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == "account"


@pytest.mark.parametrize("password", ["validpass", "A" * 30])
def test_when_password_length_valid_then_no_error_raised(password):
    # Act
    user = CreateUser(
        account="test_account",
        password=password,
        name="Test User",
        role=RoleNamesEnum.MANAGER,
    )
    # Assert
    assert user


@pytest.mark.parametrize("password", [None, "", "A" * 31])
def test_when_password_length_invalid_then_raise_validation_error(password):
    # Act
    with pytest.raises(ValidationError) as exc_info:
        CreateUser(
            account="test_account",
            password=password,
            name="Test User",
            role=RoleNamesEnum.MANAGER,
        )

    # Assert
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == "password"


@pytest.mark.parametrize("name", [None, "", "a" * 20])
def test_when_name_length_valid_then_no_error_raised(name):
    # Act
    user = CreateUser(
        id=uuid4(), account="test_account", password="valid_password", name=name, role=RoleNamesEnum.MANAGER
    )

    # Assert
    assert user


@pytest.mark.parametrize("name", ["a" * 21])
def test_when_name_length_invalid_then_raise_validation_error(name):
    # Act
    with pytest.raises(ValidationError) as exc_info:
        CreateUser(id=uuid4(), account="test_account", password="valid_password", name=name, role=RoleNamesEnum.MANAGER)

    # Assert
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == "name"


def test_when_id_not_provided_then_auto_generate_uuid():
    # Act
    user = CreateUser(
        account="test_account",
        password="valid_password",
        role=RoleNamesEnum.MANAGER,
    )

    # Assert
    assert user.id is not None


def test_when_valid_data_then_no_error_raised():
    # Act
    user = CreateUser(
        account="test_account",
        password="valid_password",
        name="Test User",
        role=RoleNamesEnum.MANAGER,
    )

    # Assert
    assert user.id is not None
    assert user.account == "test_account"
    assert user.password.get_secret_value() == "valid_password"
    assert user.name == "Test User"
    assert user.role == RoleNamesEnum.MANAGER
