from typing import Optional
from uuid import UUID

from service.model.base import AUTO_GEN_UUID4_FIELD, NAME_FIELD, BaseServiceModel, PRICE_FIELD, STOCK_FIELD


class Product(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    name: Optional[str] = NAME_FIELD
    price: Optional[float] = PRICE_FIELD
    stock: Optional[int] = STOCK_FIELD


class CreateProduct(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    name: str = NAME_FIELD
    price: float = PRICE_FIELD
    stock: int = STOCK_FIELD


class UpdateProduct(BaseServiceModel):
    name: Optional[str] = NAME_FIELD
    price: Optional[float] = PRICE_FIELD
    stock: Optional[int] = STOCK_FIELD
