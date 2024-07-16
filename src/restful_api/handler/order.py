from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query

from restful_api.context import Context
from restful_api.schema.order import Order as OrderSchema
from service.model.order import Order
from service.order import OrderService
from util.dependency_injector import get_order_service


order_router = APIRouter()


@order_router.get("/order/list", response_model=list[OrderSchema])
async def get_order_list(
    order_id_list: Optional[list[UUID]] = Query(None), order_service: OrderService = Depends(get_order_service)
):
    order_list: list[Order] = await order_service.get_order_list(order_id_list)
    return order_list


@order_router.get("/order/{order_id}", response_model=Optional[Order])
async def get_order(order_id: UUID, order_service: OrderService = Depends(get_order_service)):
    order: Order = await order_service.get_order(order_id)
    return order
