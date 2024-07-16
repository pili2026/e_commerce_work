from typing import Optional
from uuid import UUID
from repository.order import OrderRepository
from service.model.order import Order


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def get_order_list(self, order_id_list: Optional[list[UUID]] = None) -> Order:
        order_list: list[Order] = await self.order_repository.get_order_list(order_id_list)
        return order_list

    async def get_order(self, order_id: Optional[list[UUID]]) -> Order:
        order: Order = await self.order_repository.get_order(order_id)
        return order
