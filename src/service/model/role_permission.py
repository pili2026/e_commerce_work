from uuid import UUID

from service.model.base import AUTO_GEN_UUID4_FIELD, BaseServiceModel
from service.model.permission import PermissionNamesEnum
from service.model.role import RoleNamesEnum


class RolePermission(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    role: RoleNamesEnum
    permission: PermissionNamesEnum

    def to_dict(self):
        return {"id": str(self.id), "role": self.role.value, "permission": self.permission.value}


class UpdateRolePermission(BaseServiceModel):
    role: RoleNamesEnum
    permission: PermissionNamesEnum


def to_role_permission_dict(role_permission_list_model: list[RolePermission]):
    role_permission_list: list[dict] = [
        (role_permission.to_dict() if isinstance(role_permission, RolePermission) else role_permission)
        for role_permission in role_permission_list_model
    ]

    return role_permission_list
