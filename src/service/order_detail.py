from typing import Optional
from uuid import UUID
from repository.order_detail import OrderDetailRepository
from service.model.order import CreateOrder
from service.model.order_detail import CreateOrderDetail, OrderDetail, UpdateOrderDetail


class OrderDetailService:
    def __init__(self, order_detail_repository: OrderDetailRepository):
        self.order_detail_repository = order_detail_repository

    async def get_order_detail_list(self, order_detail_id_list: Optional[list[UUID]] = None) -> list[OrderDetail]:
        order_detail_list: list[OrderDetail] = await self.order_detail_repository.get_order_detail_list(
            order_detail_id_list
        )
        return order_detail_list

    async def get_order_detail(self, order_detail_id: UUID) -> OrderDetail:
        order_detail: OrderDetail = await self.order_detail_repository.get_order_detail(order_detail_id)
        return order_detail

    async def create_order_detail(
        self, create_order_detail: CreateOrderDetail, create_order: CreateOrder
    ) -> OrderDetail:
        created_order: OrderDetail = await self.order_detail_repository.insert_order_with_detail(
            create_order=create_order, create_order_detail=create_order_detail
        )
        return created_order

    async def update_order_detail(self, order_detail_id: UUID, update_order_detail: UpdateOrderDetail) -> OrderDetail:
        updated_order_detail: OrderDetail = await self.order_detail_repository.update_detail_with_product(
            order_detail_id=order_detail_id, update_order_detail=update_order_detail
        )
        return updated_order_detail
