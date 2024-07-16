from uuid import UUID

from service.model.base import BaseServiceModel


class ProductBase(BaseServiceModel):
    name: str
    price: float
    stock: int


class Product(ProductBase):
    id: UUID


class CreateProductInput(ProductBase):
    pass


class UpdateProductInput(ProductBase):
    pass
