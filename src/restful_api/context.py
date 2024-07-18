from fastapi import Depends
from strawberry.fastapi import BaseContext

from service.authentication import AuthenticationService
from service.order import OrderService
from service.order_detail import OrderDetailService
from service.product import ProductService
from service.role_permission import RolePermissionService
from service.user import UserService
from util.dependency_injector import (
    get_authentication_service,
    get_order_detail_service,
    get_order_service,
    get_role_permission_service,
    get_user_service,
    get_product_service,
)


class Context(BaseContext):
    def __init__(
        self,
        user_service: UserService,
        role_permission_service: RolePermissionService,
        product_service: ProductService,
        authentication_service: AuthenticationService,
        order_detail_service: OrderDetailService,
        order_service: OrderService,
    ):
        super().__init__()
        self.user_service = user_service
        self.role_permission_service = role_permission_service
        self.product_service = product_service
        self.authentication_service = authentication_service
        self.order_detail_service = order_detail_service
        self.order_service = order_service


def get_context(
    user_service: UserService = Depends(get_user_service),
    role_permission_service: RolePermissionService = Depends(get_role_permission_service),
    product_service: ProductService = Depends(get_product_service),
    authentication_service: AuthenticationService = Depends(get_authentication_service),
    order_detail_service: OrderDetailService = Depends(get_order_detail_service),
    order_service: OrderService = Depends(get_order_service),
):
    return Context(
        user_service=user_service,
        role_permission_service=role_permission_service,
        product_service=product_service,
        authentication_service=authentication_service,
        order_detail_service=order_detail_service,
        order_service=order_service,
    )
