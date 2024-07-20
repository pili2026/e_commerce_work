from typing import Optional
from pydantic import BaseModel
from enum import StrEnum
from uuid import UUID

from restful_api.schema.order_detail import OrderDetail
from service.model.base import BaseServiceModel


class OrderStatusEnum(StrEnum):
    PROCESSING = "processing"
    CANCELLED = "cancelled"


class Order(BaseModel):
    id: UUID
    user_id: UUID
    status: OrderStatusEnum
    detail: Optional[OrderDetail]


class UpdateOrderInput(BaseServiceModel):
    status: OrderStatusEnum
