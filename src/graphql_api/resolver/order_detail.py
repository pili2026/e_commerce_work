from typing import Optional
from uuid import UUID
import strawberry

from strawberry.types import Info

from graphql_api.schema.order_detail import CreateOrderDetailInput
from service.model.order import CreateOrder
from service.model.order_detail import CreateOrderDetail, OrderDetail
from graphql_api.schema.order_detail import OrderDetail as OrderDetailSchema
from service.order_detail import OrderDetailService


@strawberry.type
class OrderDetailQuery:
    @strawberry.field
    async def get_order_detail_list(
        self, info: Info, order_detail_id: Optional[list[UUID]] = None
    ) -> Optional[list[OrderDetailSchema]]:
        order_detail_service: OrderDetailService = info.context.order_detail_service
        order_detail_list: list[OrderDetail] = await order_detail_service.get_order_detail_list(order_detail_id)
        return order_detail_list

    @strawberry.field
    async def get_order_detail(self, info: Info, order_detail_id: UUID = None) -> Optional[OrderDetailSchema]:
        order_detail_service: OrderDetailService = info.context.order_detail_service
        order_detail: OrderDetail = await order_detail_service.get_order_detail(order_detail_id)
        return order_detail


@strawberry.type
class OrderDetailMutation:
    @strawberry.mutation
    async def create_order_detail(self, info: Info, order_detail: CreateOrderDetailInput) -> OrderDetailSchema:
        order_detail_service: OrderDetailService = info.context.order_detail_service

        create_order: CreateOrder = CreateOrder()
        create_order_detail = CreateOrderDetail(product_name=order_detail.product_name, quantity=order_detail.quantity)

        created_order_detail: OrderDetail = await order_detail_service.create_order_detail(
            create_order_detail=create_order_detail, create_order=create_order
        )
        return created_order_detail
