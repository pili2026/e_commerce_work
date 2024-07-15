# pylint: disable=import-error

from service.model.role import RoleNamesEnum
from service.model.role_permission import PermissionNamesEnum, RolePermission


SYSTEM_ROLE_PERMISSION_LIST: list[RolePermission] = [
    RolePermission(
        role=RoleNamesEnum.MANAGER,
        permission=PermissionNamesEnum.CREATE_PRODUCT,
    ),
    RolePermission(
        role=RoleNamesEnum.MANAGER,
        permission=PermissionNamesEnum.READ_PRODUCT,
    ),
    RolePermission(
        role=RoleNamesEnum.MANAGER,
        permission=PermissionNamesEnum.UPDATE_PRODUCT,
    ),
    RolePermission(
        role=RoleNamesEnum.MANAGER,
        permission=PermissionNamesEnum.DELETE_PRODUCT,
    ),
    RolePermission(
        role=RoleNamesEnum.MANAGER,
        permission=PermissionNamesEnum.READ_ALL_ORDERS,
    ),
    RolePermission(
        role=RoleNamesEnum.CUSTOMER,
        permission=PermissionNamesEnum.CREATE_ORDER,
    ),
    RolePermission(
        role=RoleNamesEnum.CUSTOMER,
        permission=PermissionNamesEnum.READ_OWN_ORDER,
    ),
    RolePermission(
        role=RoleNamesEnum.CUSTOMER,
        permission=PermissionNamesEnum.UPDATE_ORDER,
    ),
    RolePermission(
        role=RoleNamesEnum.CUSTOMER,
        permission=PermissionNamesEnum.DELETE_ORDER,
    ),
]