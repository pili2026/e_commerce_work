from typing import Optional
from uuid import UUID

import strawberry
from strawberry.types import Info

from graphql_api.data_loader.role_permission_list_mapping_data_loader import RolePermissionLoader
from graphql_api.schema.permission import RolePermissionList
from service.model.role import RoleNamesEnum
from service.model.role_permission import RolePermission as RolePermissionModel
from util.validation_utils import validate_input_length


@strawberry.type
class User:
    id: UUID
    account: str
    name: Optional[str]
    role: RoleNamesEnum

    @strawberry.field
    async def role_permission_list(self, info: Info) -> list[RolePermissionList]:
        role_permission_loader: RolePermissionLoader = info.context.role_permission_loader
        role_permission_list: list[RolePermissionModel] = await role_permission_loader.load(self.role)
        return role_permission_list


@strawberry.input
class CreateUserInput:
    account: str
    name: Optional[str]
    password: str
    role: RoleNamesEnum

    def __init__(self, account: str, password: str, role: RoleNamesEnum, name: Optional[str] = None):
        # TODO: The next phase is to add validation map for each keyword.
        self.account = validate_input_length(value=account, min_length=0, max_length=20)
        self.name = validate_input_length(value=name, min_length=0, max_length=20) if name is not None else None
        self.password = validate_input_length(value=password, min_length=0, max_length=50)
        self.role = role


@strawberry.input
class UpdateUserInput:
    name: str
    role: RoleNamesEnum
