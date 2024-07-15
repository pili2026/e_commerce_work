from uuid import UUID, uuid4

from repository.role_permission import RolePermissionRepository
from service.model.role import RoleNamesEnum
from service.model.role_permission import PermissionNamesEnum, RolePermission, UpdateRolePermission


class RolePermissionService:
    def __init__(self, role_permission_repository: RolePermissionRepository):
        self.role_permissions_repository = role_permission_repository

    async def get_role_permission_list(self, role_list: list[RoleNamesEnum]) -> list[RolePermission]:
        role_permissions: list[RolePermission] = await self.role_permissions_repository.get_role_permission_list(
            role_list=role_list
        )
        return role_permissions

    async def get_role_permission(self, role: RoleNamesEnum, permission: PermissionNamesEnum) -> RolePermission:
        role_permission = await self.role_permissions_repository.get_role_permission(role=role, permission=permission)
        return role_permission

    async def create_role_permission(self, role_permission: RolePermission) -> RolePermission:
        role_permission.id = uuid4()
        created_role_permission = await self.role_permissions_repository.insert_role_permission(role_permission)
        return created_role_permission

    async def update_role_permission(
        self, role_permission_id: UUID, role_permission: UpdateRolePermission
    ) -> RolePermission:
        updated_role_permission = await self.role_permissions_repository.update_role_permission(
            role_permission_id, role_permission
        )
        return updated_role_permission
