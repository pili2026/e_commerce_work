from uuid import UUID

from service.model.base import BaseServiceModel
from service.model.permission import PermissionNamesEnum
from service.model.role import RoleNamesEnum


class RolePermissionList(BaseServiceModel):
    id: UUID
    role: RoleNamesEnum
    permission: PermissionNamesEnum
