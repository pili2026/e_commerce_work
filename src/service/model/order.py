from enum import StrEnum
from uuid import UUID
from typing import Optional

import strawberry

from service.model.base import AUTO_GEN_UUID4_FIELD, BaseServiceModel
from service.model.order_detail import OrderDetail, UpdateOrderDetail


@strawberry.enum
class OrderStatusEnum(StrEnum):
    PROCESSING = "processing"
    CANCELLED = "cancelled"


class Order(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    user_id: UUID
    status: OrderStatusEnum
    # details: Optional[list[OrderDetail]]


class CreateOrder(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    user_id: UUID = UUID("be91692a-a0c9-42bd-a4fb-c8f7f3bae470")
    status: OrderStatusEnum = OrderStatusEnum.PROCESSING


class UpdateOrder(BaseServiceModel):
    details: Optional[list[UpdateOrderDetail]]
