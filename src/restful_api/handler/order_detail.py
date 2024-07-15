from fastapi import APIRouter, Depends

from restful_api.schema.order_detail import CreateOrderDetailInput as CreateOrderDetailInputSchema
from service.model.order import CreateOrder
from service.model.order_detail import CreateOrderDetail, OrderDetail
from service.order_detail import OrderDetailService
from util.dependency_injector import get_order_detail_service


order_detail_router = APIRouter()


@order_detail_router.post("/order_detail", response_model=OrderDetail)
async def create_order_detail(
    create_order_detail: CreateOrderDetailInputSchema,
    order_detail_service: OrderDetailService = Depends(get_order_detail_service),
):
    create_order: CreateOrder = CreateOrder()
    create_order_detail = CreateOrderDetail(
        product_name=create_order_detail.product_name, quantity=create_order_detail.quantity
    )

    created_order_detail = await order_detail_service.create_order_detail(
        create_order_detail=create_order_detail, create_order=create_order
    )
    return created_order_detail
