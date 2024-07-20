from enum import StrEnum
from uuid import UUID
from typing import Optional


from service.model.base import AUTO_GEN_UUID4_FIELD, BaseServiceModel
from service.model.order_detail import OrderDetail


class OrderStatusEnum(StrEnum):
    DONE = "Done"
    PROCESSING = "Processing"
    CANCEL = "Cancel"
    CANCELLED = "Cancelled"


class Order(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    user_id: UUID
    status: OrderStatusEnum
    detail: Optional[OrderDetail]


class CreateOrder(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    user_id: UUID
    status: OrderStatusEnum = OrderStatusEnum.PROCESSING


class UpdateOrder(BaseServiceModel):
    status: OrderStatusEnum
