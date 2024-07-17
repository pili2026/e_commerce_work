import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import ChunkedIteratorResult, Select, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.future import select

from repository.model.product import ProductDBModel
from repository.postgres_error_code.integrity_error_code import IntegrityErrorCode
from service.model.product import CreateProduct, Product, UpdateProduct
from util.app_error import AppError, ErrorCode, ServiceException
from util.db_manager import DBManager


log = logging.getLogger(__name__)


class ProductRepository:

    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    async def get_product_list(self, product_id_list: Optional[UUID] = None) -> list[Product]:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                query: Select = select(ProductDBModel)

                if product_id_list:
                    query: Select = query.where(ProductDBModel.id.in_(product_id_list))

                result: ChunkedIteratorResult = await db_session.execute(query)
                product_db_model_list: list[ProductDBModel] = result.scalars().all()
                return [product_db_model.to_service_model() for product_db_model in product_db_model_list]

    async def get_product(self, product_id: Optional[UUID] = None, product_name: Optional[str] = None) -> Product:
        if not product_id and not product_name:
            raise ServiceException(
                code=400,
                message="At least one parameter (product_id, or product_name) must be provided",
            )

        async with self.db_manager.get_async_session() as db_session:
            try:
                query = select(ProductDBModel)
                if product_id:
                    query = query.filter(ProductDBModel.id == product_id)
                if product_name:
                    query = query.filter(ProductDBModel.name == product_name)

                result = await db_session.execute(query)
                product_db_model: ProductDBModel = result.scalars().one()
                return product_db_model.to_service_model()
            except NoResultFound as e:
                self._handle_not_found_error(product_id, e)

    async def insert_product(self, product: CreateProduct) -> Product:
        async with self.db_manager.get_async_session() as db_session:
            try:
                async with db_session.begin():
                    product_db_model = ProductDBModel(
                        id=product.id,
                        name=product.name,
                        stock=product.stock,
                        price=product.price,
                    )
                    db_session.add(product_db_model)
                    return product_db_model.to_service_model()
            except IntegrityError as e:
                self._handle_integrity_error(e)

    async def update_product(self, product_id: UUID, update_product: UpdateProduct) -> Product:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                try:
                    query = select(ProductDBModel).filter(ProductDBModel.id == product_id)
                    result = await db_session.execute(query)
                    product_db_model: ProductDBModel = result.scalars().one()

                    product_db_model.name = update_product.name
                    product_db_model.price = update_product.price
                    product_db_model.stock = update_product.stock
                    return product_db_model.to_service_model()
                except NoResultFound as e:
                    self._handle_not_found_error(product_id, e)

    async def delete_product(self, product_id: UUID) -> bool:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                await db_session.execute(delete(ProductDBModel).where(ProductDBModel.id == product_id))
                return True

    def _handle_not_found_error(self, product_id, e):
        err_msg = f"No product found with id {product_id}."
        log.error(err_msg)
        raise ServiceException(message=err_msg, code=404) from e

    def _handle_integrity_error(self, e):
        if e.orig.pgcode == IntegrityErrorCode.UNIQUE_VIOLATION.value:
            raise ServiceException(
                message="Product name already exists.",
                code=409,
            ) from e
        raise e from e
