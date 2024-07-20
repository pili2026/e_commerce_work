from uuid import UUID
from fastapi import APIRouter, Depends

from restful_api.schema.order_detail import (
    CreateOrderDetailInput as CreateOrderDetailInputSchema,
    UpdateOrderDetailInput,
)
from service.model.order import CreateOrder
from service.model.order_detail import CreateOrderDetail, OrderDetail, UpdateOrderDetail
from service.model.role import RoleNamesEnum
from service.order_detail import OrderDetailService
from util.authentication import check_permissions
from util.dependency_injector import get_order_detail_service


order_detail_router = APIRouter()


@order_detail_router.post("/order_detail", response_model=OrderDetail)
async def create_order_detail(
    create_order_detail: CreateOrderDetailInputSchema,
    order_detail_service: OrderDetailService = Depends(get_order_detail_service),
    current_user: dict = Depends(check_permissions(RoleNamesEnum.CUSTOMER.value)),
):
    create_order: CreateOrder = CreateOrder(user_id=current_user["sub"])
    create_order_detail = CreateOrderDetail(
        product_name=create_order_detail.product_name, quantity=create_order_detail.quantity
    )

    created_order_detail: OrderDetail = await order_detail_service.create_order_detail(
        create_order_detail=create_order_detail, create_order=create_order
    )
    return created_order_detail


@order_detail_router.put("/order_detail/{order_detail_id}", response_model=OrderDetail)
async def update_order_detail(
    order_detail_id: UUID,
    update_order_detail: UpdateOrderDetailInput,
    order_detail_service: OrderDetailService = Depends(get_order_detail_service),
    _: dict = Depends(check_permissions(RoleNamesEnum.CUSTOMER.value)),
):
    update_order_detail = UpdateOrderDetail(
        product_name=update_order_detail.product_name, quantity=update_order_detail.quantity
    )

    updated_order_detail: OrderDetail = await order_detail_service.update_order_detail(
        order_detail_id=order_detail_id, update_order_detail=update_order_detail
    )
    return updated_order_detail
