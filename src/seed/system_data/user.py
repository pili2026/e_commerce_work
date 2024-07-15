# pylint: disable=import-error

from service.model.role import RoleNamesEnum
from service.model.user import CreateUser


SYSTEM_USER_LIST: list[CreateUser] = [
    CreateUser(
        account="manager",
        password="manager1234",
        name="Default Manager",
        role=RoleNamesEnum.MANAGER,
    ),
    CreateUser(
        account="customer",
        password="customer1234",
        name="Default Customer",
        role=RoleNamesEnum.CUSTOMER,
    ),
]
