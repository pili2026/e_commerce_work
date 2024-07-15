from typing import Optional
from uuid import UUID

import strawberry
from strawberry.types import Info

from graphql_api.decorator.authentication import validate_jwt_token
from graphql_api.schema.product import CreateProductInput, UpdateProductInput, Product as ProductSchema
from service.model.product import CreateProduct, Product, UpdateProduct
from service.product import ProductService


@strawberry.type
class ProductQuery:
    @strawberry.field
    async def get_product_list(
        self, info: Info, product_id_list: Optional[list[UUID]] = None
    ) -> Optional[list[ProductSchema]]:
        product_service: ProductService = info.context.product_service
        product_list: list[Product] = await product_service.get_product_list(product_id_list)
        return product_list

    @strawberry.field
    async def get_product(self, info: Info, product_id: UUID = None) -> Optional[ProductSchema]:
        product_service: ProductService = info.context.product_service
        product: Product = await product_service.get_product_by_id(product_id)
        return product


@strawberry.type
class ProductMutation:
    @strawberry.mutation
    async def create_product(self, info: Info, product: CreateProductInput) -> ProductSchema:
        product_service: ProductService = info.context.product_service
        create_product_model = CreateProduct(name=product.name, price=product.price, stock=product.stock)
        created_product: Product = await product_service.create_product(create_product_model)
        return created_product

    @strawberry.mutation
    async def update_product(self, info: Info, product_id: UUID, product: UpdateProductInput) -> ProductSchema:
        product_service: ProductService = info.context.product_service

        update_product_model = UpdateProduct(name=product.name, price=product.price, stock=product.stock)
        updated_product: Product = await product_service.update_product(
            product_id=product_id, update_product=update_product_model
        )
        return updated_product

    @strawberry.mutation
    async def delete_product(self, info: Info, product_id: UUID) -> bool:
        product_service: ProductService = info.context.product_service
        result: bool = await product_service.delete_product(product_id)
        return result
