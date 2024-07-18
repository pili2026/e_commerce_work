# pylint: disable=import-error
import logging

from repository.product import ProductRepository
from repository.role_permission import RolePermissionRepository
from repository.user import UserRepository
from seed.system_data.product import SYSTEM_PRODUCT_LIST
from seed.system_data.role_permission import SYSTEM_ROLE_PERMISSION_LIST
from seed.system_data.user import SYSTEM_USER_LIST
from service.model.product import CreateProduct
from service.model.role_permission import RolePermission, UpdateRolePermission
from service.model.user import CreateUser
from service.product import ProductService
from service.role_permission import RolePermissionService
from service.user import UserService
from util.app_error import ServiceException, ErrorCode, ServiceException
from util.db_manager import get_db_manager


log = logging.getLogger(__name__)


class AppDefaultDataGenerator:
    def __init__(
        self, user_service: UserService, role_permission_service: RolePermissionService, product_service: ProductService
    ):
        self.__user_service = user_service
        self.__role_permission_service = role_permission_service
        self.__product_service = product_service

    async def generate_app_default_data(self):
        log.info("Generating system data...")
        await self.__generate_role_permission_default_data()
        await self.__generate_user_default_data()
        await self.__generate_product_default_data()

    async def __generate_user_default_data(self):
        log.info("Generating user system data...")

        # TODO: Use bulk insert
        for user in SYSTEM_USER_LIST:
            await self.__create_user(user)

    async def __generate_role_permission_default_data(self):
        log.info("Generating role permission system data...")

        # TODO: Use bulk insert
        for role_permission in SYSTEM_ROLE_PERMISSION_LIST:
            await self.__create_or_update_role_permission(role_permission)

    async def __generate_product_default_data(self):
        log.info("Generating product system data...")

        # TODO: Product bulk insert
        for product in SYSTEM_PRODUCT_LIST:
            await self.__create_product(product)

    async def __create_user(self, user: CreateUser):
        existing_user = None
        try:
            existing_user = await self.__user_service.get_user_by_account(user.account)
        except ServiceException as e:
            if e.status_code == ErrorCode.NOT_FOUND:
                existing_user = None

        if existing_user is None:
            created_user = await self.__user_service.create_user(user)
            log.info(f"The user, {created_user} has been created.")

    async def __create_or_update_role_permission(self, role_permission: RolePermission):
        try:
            existing_role_permission = await self.__role_permission_service.get_role_permission(
                role_permission.role, role_permission.permission
            )
        except ServiceException as e:
            if e.code == ErrorCode.NOT_FOUND:
                existing_role_permission = None

        if existing_role_permission is None:
            created_role_permission = await self.__role_permission_service.create_role_permission(role_permission)
            log.info(f"The role_permission, {created_role_permission} has been created.")
        else:
            permission_to_update = UpdateRolePermission(
                role=role_permission.role, permission=role_permission.permission
            )
            updated_role_permission = await self.__role_permission_service.update_role_permission(
                existing_role_permission.id,
                permission_to_update,
            )
            log.info(f"The role_permission, {updated_role_permission} has been updated.")

    async def __create_product(self, product: CreateProduct):
        try:
            existing_product = await self.__product_service.get_product_by_name(product.name)
        except ServiceException as e:
            if e.status_code == ErrorCode.NOT_FOUND:
                existing_product = None

        if existing_product is None:
            created_product = await self.__product_service.create_product(product)
            log.info(f"The product, {created_product} has been created.")


def get_app_default_data_generator():
    db_manager = get_db_manager()
    role_permission_repo = RolePermissionRepository(db_manager)
    user_repo = UserRepository(db_manager, role_permission_repo)
    product_repo = ProductRepository(db_manager)
    user_service = UserService(user_repo)
    role_permission_service = RolePermissionService(role_permission_repo)
    product_service = ProductService(product_repo)

    return AppDefaultDataGenerator(
        user_service=user_service, role_permission_service=role_permission_service, product_service=product_service
    )
