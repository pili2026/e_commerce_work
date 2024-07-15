from uuid import UUID
from typing import Optional

from service.model.base import AUTO_GEN_UUID4_FIELD, NAME_FIELD, PRICE_FIELD, STOCK_FIELD, BaseServiceModel


class OrderDetail(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    order_id: UUID
    product_id: UUID
    product_name: str = NAME_FIELD
    product_price: float = PRICE_FIELD
    quantity: int = STOCK_FIELD
    total_price: float = PRICE_FIELD


class CreateOrderDetail(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    order_id: UUID = None
    product_name: str = NAME_FIELD
    quantity: int = STOCK_FIELD


class UpdateOrderDetail(BaseServiceModel):
    product_name: Optional[str]
    quantity: Optional[int]
