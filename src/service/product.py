from typing import Optional
from uuid import UUID

from repository.product import ProductRepository
from service.model.product import CreateProduct, Product, UpdateProduct


class ProductService:

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_product(self, product_id: Optional[UUID] = None, product_name: Optional[str] = None) -> Product:
        product: Product = await self.product_repository.get_product(product_id=product_id, product_name=product_name)
        return product

    async def get_product_list(self, product_id_list: Optional[list[UUID]] = None) -> list[Product]:
        product_list: list[Product] = await self.product_repository.get_product_list(product_id_list)
        return product_list

    async def create_product(self, create_product: CreateProduct) -> Product:
        created_product: Product = await self.product_repository.insert_product(create_product)
        return created_product

    async def update_product(self, product_id: UUID, update_product: UpdateProduct) -> Product:
        updated_product: Product = await self.product_repository.update_product(
            product_id=product_id, update_product=update_product
        )
        return updated_product

    async def delete_product(self, product_id: UUID) -> bool:
        result = await self.product_repository.delete_product(product_id)
        return result
