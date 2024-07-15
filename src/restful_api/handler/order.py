from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from graphql_api.context import Context, get_context
from restful_api.schema.order import Order as OrderSchema
from service.model.order import Order
from service.order import OrderService


order_router = APIRouter()


@order_router.get("/order/list", response_model=list[OrderSchema])
async def get_order_list(order_id_list: Optional[list[UUID]] = Query(None), context: Context = Depends(get_context)):
    order_service: OrderService = context.order_service
    order_list: list[Order] = await order_service.get_order_list(order_id_list)
    return order_list
