from uuid import UUID

import strawberry


@strawberry.type
class ProductBase:
    name: str
    price: float
    stock: int


@strawberry.type
class Product(ProductBase):
    id: UUID


@strawberry.type
class CreateProduct(ProductBase):
    pass


@strawberry.input
class UpdateProductInput(ProductBase):
    pass


from uuid import UUID

import strawberry


@strawberry.type
class ProductBase:
    name: str
    price: float
    stock: int


@strawberry.type
class Product(ProductBase):
    id: UUID


@strawberry.input
class CreateProductInput(ProductBase):
    pass


@strawberry.input
class UpdateProductInput(ProductBase):
    pass
