from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status

from restful_api.schema.product import CreateProductInput, Product as ProductSchema, UpdateProductInput
from service.model.product import CreateProduct, Product, UpdateProduct
from service.model.role import RoleNamesEnum
from service.product import ProductService
from util.authentication import check_permissions
from util.dependency_injector import get_product_service


product_router = APIRouter()


@product_router.post("/product/list", response_model=list[ProductSchema])
async def get_product_list(
    product_id_list: Optional[list[UUID]] = None, product_service: ProductService = Depends(get_product_service)
):
    product_list: list[Product] = await product_service.get_product_list(product_id_list)
    return product_list


@product_router.get("/product/{product_id}", response_model=ProductSchema)
async def get_product(product_id: UUID, product_service: ProductService = Depends(get_product_service)):
    product: Product = await product_service.get_product_by_id(product_id)
    return product


@product_router.post("/product", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: CreateProductInput,
    product_service: ProductService = Depends(get_product_service),
    _: dict = Depends(check_permissions(RoleNamesEnum.MANAGER.value)),  # TODO:Confirm the usage principle of StrEnum
):
    create_product_model = CreateProduct(name=product.name, price=product.price, stock=product.stock)
    created_product: Product = await product_service.create_product(create_product_model)
    return created_product


@product_router.put("/product/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: UUID, product: UpdateProductInput, product_service: ProductService = Depends(get_product_service)
):
    update_product_model = UpdateProduct(name=product.name, price=product.price, stock=product.stock)
    updated_product: Product = await product_service.update_product(
        product_id=product_id, update_product=update_product_model
    )
    return updated_product


@product_router.delete("/product/{product_id}", response_model=bool)
async def delete_product(product_id: UUID, product_service: ProductService = Depends(get_product_service)):
    result: bool = await product_service.delete_product(product_id)
    return result
