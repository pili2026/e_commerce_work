from strawberry.dataloader import DataLoader

from service.model.role import RoleNamesEnum
from service.model.role_permission import RolePermission as RolePermissionModel
from service.role_permission import RolePermissionService


class RolePermissionLoader(DataLoader):
    def __init__(self, role_permission_service: RolePermissionService):
        super().__init__(load_fn=self.batch_load_unique_role_permission_list)
        self.role_permission_service = role_permission_service

    async def batch_load_unique_role_permission_list(self, role_list: list[RoleNamesEnum]) -> list[RolePermissionModel]:
        role_permission_list: list[RolePermissionModel] = await self.role_permission_service.get_role_permission_list(
            role_list=role_list
        )

        role_map = {role: [] for role in role_list}
        for role_permission in role_permission_list:
            role_map[role_permission.role].append(role_permission)

        return [role_map[role] for role in role_list]
