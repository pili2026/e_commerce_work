from typing import Optional
from uuid import UUID

import strawberry
from strawberry.types import Info

from graphql_api.schema.order import Order as OrderSchema
from service.model.order import Order
from service.order import OrderService


@strawberry.type
class OrderQuery:
    @strawberry.field
    async def get_order_list(
        self, info: Info, order_id_list: Optional[list[UUID]] = None
    ) -> Optional[list[OrderSchema]]:
        order_service: OrderService = info.context.order_service
        order_list: list[Order] = await order_service.get_order_list(order_id_list)
        return order_list

    @strawberry.field
    async def get_order(self, info: Info, order_id: UUID) -> Optional[OrderSchema]:
        order_service: OrderService = info.context.order_service
        order: Order = await order_service.get_order(order_id)
        return order
