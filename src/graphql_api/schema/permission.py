from uuid import UUID

import strawberry

from service.model.permission import PermissionNamesEnum
from service.model.role import RoleNamesEnum


@strawberry.type
class RolePermissionList:
    id: UUID
    role: RoleNamesEnum
    permission: PermissionNamesEnum
