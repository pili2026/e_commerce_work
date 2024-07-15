from uuid import UUID

from service.model.base import AUTO_GEN_UUID4_FIELD, BaseServiceModel
from service.model.permission import PermissionNamesEnum
from service.model.role import RoleNamesEnum


class RolePermission(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    role: RoleNamesEnum
    permission: PermissionNamesEnum


class UpdateRolePermission(BaseServiceModel):
    role: RoleNamesEnum
    permission: PermissionNamesEnum
