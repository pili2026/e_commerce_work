from typing import Optional
from pydantic import BaseModel

from uuid import UUID

from restful_api.schema.order_detail import OrderDetail
from service.model.order import OrderStatusEnum
from service.model.base import BaseServiceModel


class Order(BaseModel):
    id: UUID
    user_id: UUID
    status: OrderStatusEnum
    detail: Optional[OrderDetail]


class UpdateOrderInput(BaseServiceModel):
    status: OrderStatusEnum
