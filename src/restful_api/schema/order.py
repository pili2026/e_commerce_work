from pydantic import BaseModel
from enum import StrEnum
from uuid import UUID


class OrderStatusEnum(StrEnum):
    PROCESSING = "processing"
    CANCELLED = "cancelled"


class Order(BaseModel):
    id: UUID
    user_id: UUID
    status: OrderStatusEnum
