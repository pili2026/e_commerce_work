from typing import Optional
from uuid import UUID
from repository.order import OrderRepository
from service.model.order import Order, UpdateOrder


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def get_order_list(
        self, order_id_list: Optional[list[UUID]] = None, user_id: Optional[list[UUID]] = None
    ) -> Order:
        order_list: list[Order] = await self.order_repository.get_order_list(
            order_id_list=order_id_list, user_id=user_id
        )
        return order_list

    async def get_order(self, order_id: Optional[list[UUID]] = None, user_id: Optional[UUID] = None) -> Order:
        order: Order = await self.order_repository.get_order(order_id=order_id, user_id=user_id)
        return order

    async def update_order(self, order_id: UUID, update_order: UpdateOrder) -> Order:
        updated_order: Order = await self.order_repository.update_order(order_id=order_id, update_order=update_order)
        return updated_order

    async def delete_order(self, order_id: UUID) -> bool:
        result: bool = await self.order_repository.delete_order(order_id)
        return result
