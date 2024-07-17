import logging

from fastapi import Depends

from graphql_api.data_loader.role_permission_list_mapping_data_loader import RolePermissionLoader
from repository.auth_session import AuthSessionRepository
from repository.order import OrderRepository
from repository.order_detail import OrderDetailRepository
from repository.product import ProductRepository
from repository.role_permission import RolePermissionRepository
from repository.user import UserRepository
from service.authentication import AuthenticationService
from service.order import OrderService
from service.order_detail import OrderDetailService
from service.product import ProductService
from service.role_permission import RolePermissionService
from service.user import UserService
from util.config_manager import ConfigManager, get_config_manager
from util.db_manager import DBManager, get_db_manager


log = logging.getLogger(__name__)


def get_role_permission_repository(db_manager: DBManager = Depends(get_db_manager)) -> RolePermissionRepository:
    return RolePermissionRepository(db_manager)


def get_role_permission_service(
    role_permission_repository: RolePermissionRepository = Depends(get_role_permission_repository),
) -> RolePermissionService:
    return RolePermissionService(role_permission_repository=role_permission_repository)


def get_user_repository(
    db_manager: DBManager = Depends(get_db_manager),
    role_permission_repository: RolePermissionRepository = Depends(get_role_permission_repository),
) -> UserRepository:
    return UserRepository(db_manager=db_manager, role_permission_repository=role_permission_repository)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)


async def get_role_permission_loader(
    role_permission_service: RolePermissionService = Depends(get_role_permission_service),
) -> RolePermissionLoader:
    return RolePermissionLoader(role_permission_service=role_permission_service)


def get_product_repository(db_manager: DBManager = Depends(get_db_manager)) -> ProductRepository:
    return ProductRepository(db_manager)


def get_product_service(product_repository: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(product_repository)


def get_auth_session_repository(db_manager: DBManager = Depends(get_db_manager)) -> AuthSessionRepository:
    return AuthSessionRepository(db_manager=db_manager)


def get_authentication_service(
    session_repository: AuthSessionRepository = Depends(get_auth_session_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    config_manager: ConfigManager = Depends(get_config_manager),
) -> AuthenticationService:
    return AuthenticationService(session_repository, user_repository, config_manager)


def get_order_repository(db_manager: DBManager = Depends(get_db_manager)) -> OrderRepository:
    return OrderRepository(db_manager=db_manager)


def get_order_service(order_repository: OrderRepository = Depends(get_order_repository)) -> OrderService:
    return OrderService(order_repository)


def get_order_detail_repository(
    db_manager: DBManager = Depends(get_db_manager),
    order_repository: OrderDetailRepository = Depends(get_order_repository),
) -> OrderDetailService:
    return OrderDetailRepository(db_manager=db_manager, order_repository=order_repository)


def get_order_detail_service(
    order_detail_repository: OrderDetailRepository = Depends(get_order_detail_repository),
) -> OrderDetailService:
    return OrderDetailService(order_detail_repository=order_detail_repository)
