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
    user_id: UUID = UUID("4a0e208c-72ea-4fbb-a59f-208be7208dc2")
    status: OrderStatusEnum = OrderStatusEnum.PROCESSING


class UpdateOrder(BaseServiceModel):
    details: Optional[list[UpdateOrderDetail]]
