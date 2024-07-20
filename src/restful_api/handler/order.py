from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from restful_api.schema.order import Order as OrderSchema, UpdateOrderInput
from service.model.order import Order, UpdateOrder
from service.model.role import RoleNamesEnum
from service.order import OrderService
from util.app_error import ErrorCode, ServiceException
from util.authentication import check_permissions, check_status_permission, get_current_user
from util.dependency_injector import get_order_service


order_router = APIRouter()


@order_router.post("/order/list", response_model=list[OrderSchema])
async def get_order_list(
    order_id_list: Optional[list[UUID]] = None,
    order_service: OrderService = Depends(get_order_service),
    current_user: dict = Depends(get_current_user),
):
    if RoleNamesEnum.CUSTOMER.value in current_user["role"]:
        order_list: list[Order] = await order_service.get_order_list(user_id=[current_user["sub"]])
    elif RoleNamesEnum.MANAGER.value in current_user["role"]:
        order_list: list[Order] = await order_service.get_order_list(order_id_list=order_id_list)
    else:
        raise ServiceException(status_code=ErrorCode.INVALID_PERMISSION, detail="Operation not permitted")

    return order_list


@order_router.get("/order/{order_id}", response_model=Optional[Order])
async def get_order(
    order_id: UUID,
    order_service: OrderService = Depends(get_order_service),
    current_user: dict = Depends(get_current_user),
):
    order: Order = await order_service.get_order(order_id)

    if RoleNamesEnum.CUSTOMER.value in current_user["role"] and order.user_id != current_user["sub"]:
        raise ServiceException(status_code=ErrorCode.INVALID_PERMISSION, detail="Operation not permitted")

    return order


@order_router.put("/order/{order_id}", response_model=Order)
async def update_order(
    order_id: UUID,
    order: UpdateOrderInput,
    order_service: OrderService = Depends(get_order_service),
    current_user: dict = Depends(check_permissions(RoleNamesEnum.MANAGER.value)),
):

    role: str = current_user.get("role")
    check_status_permission(role=role, order_status=order.status)

    update_order_model = UpdateOrder(status=order.status)
    updated_order: Order = await order_service.update_order(order_id=order_id, update_order=update_order_model)
    return updated_order


@order_router.delete("/order/{order_id}", response_model=bool)
async def delete_order(
    order_id: UUID,
    order_service: OrderService = Depends(get_order_service),
    _: dict = Depends(check_permissions(RoleNamesEnum.MANAGER.value)),
):
    result: bool = await order_service.delete_order(order_id=order_id)
    return result
