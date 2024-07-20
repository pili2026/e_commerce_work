import logging
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ChunkedIteratorResult, Select, delete
from sqlalchemy.exc import IntegrityError, NoResultFound

from sqlalchemy.future import select

from repository.model.order import OrderDBModel
from repository.model.order_detail import OrderDetailDBModel
from repository.model.product import ProductDBModel
from repository.order import OrderRepository
from repository.postgres_error_code.integrity_error_code import IntegrityErrorCode
from service.model.order import CreateOrder
from service.model.order_detail import CreateOrderDetail, OrderDetail, UpdateOrderDetail
from util.app_error import ServiceException, ErrorCode, ServiceException
from util.db_manager import DBManager


log = logging.getLogger(__name__)


class OrderDetailRepository:

    def __init__(self, db_manager: DBManager, order_repository: OrderRepository):
        self.db_manager = db_manager
        self.order_repository = order_repository

    async def get_order_detail_list(self, order_detail_id_list: Optional[UUID] = None) -> list[OrderDetail]:
        async with self.db_manager.get_async_session() as db_session:
            query: Select = select(OrderDetailDBModel)

            if order_detail_id_list:
                query: Select = query.where(OrderDetailDBModel.id.in_(order_detail_id_list))

            result: ChunkedIteratorResult = await db_session.execute(query)
            order_detail_db_model_list: list[OrderDetailDBModel] = result.scalars().all()
            return [order_detail_db_model.to_service_model() for order_detail_db_model in order_detail_db_model_list]

    async def get_order_detail(self, order_detail_id: Optional[UUID] = None) -> OrderDetail:
        if not order_detail_id:
            raise ServiceException(
                code=ErrorCode.INVALID_FORMAT,
                message="The order_detail_id is required",
            )

        async with self.db_manager.get_async_session() as db_session:
            try:
                query: Select = select(OrderDetailDBModel)
                query = query.filter(OrderDetailDBModel.id == order_detail_id)

                result: ChunkedIteratorResult = await db_session.execute(query)
                order_detail_db_model: OrderDetailDBModel = result.scalars().one()
                return order_detail_db_model.to_service_model()
            except NoResultFound as e:
                self._handle_not_found_error(order_detail_id, e)

    async def create_order_detail_db_model(
        self, order_detail: CreateOrderDetail, product: ProductDBModel
    ) -> OrderDetailDBModel:
        try:
            if product.stock < order_detail.quantity:
                err_msg = f"Not enough stock for product {order_detail.product_name}. Available: {product.stock}, Requested: {order_detail.quantity}."
                raise ServiceException(message=err_msg, code=ErrorCode.INSUFFICIENT_STOCK)

            order_detail_db_model = OrderDetailDBModel(
                id=order_detail.id,
                order_id=order_detail.order_id,
                product_id=product.id,
                product_name=order_detail.product_name,
                product_price=product.price,
                quantity=order_detail.quantity,
                total_price=product.price * order_detail.quantity,
            )
            return order_detail_db_model
        except IntegrityError as e:
            self._handle_integrity_error(e)
            raise

    async def get_product_by_order_detail(self, product_name: str, db_session: AsyncSession) -> ProductDBModel:
        product_query = select(ProductDBModel).where(ProductDBModel.name == product_name)
        result: ChunkedIteratorResult = await db_session.execute(product_query)
        product: ProductDBModel = result.scalar_one_or_none()

        if not product:
            err_msg = f"No product found with product {product_name}."
            raise ServiceException(message=err_msg, code=ErrorCode.NOT_FOUND)

        if product.stock <= 0:
            err_msg = f"Product {product_name} is out of stock."
            raise ServiceException(message=err_msg, code=ErrorCode.OUT_OF_STOCK)

        return product

    async def insert_order_with_detail(
        self, create_order: CreateOrder, create_order_detail: CreateOrderDetail
    ) -> OrderDetail:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                try:
                    order_db_model: OrderDBModel = await self.order_repository.create_order_db_model(create_order)
                    create_order_detail.order_id = order_db_model.id
                    product: ProductDBModel = await self.get_product_by_order_detail(
                        product_name=create_order_detail.product_name, db_session=db_session
                    )

                    order_detail_db_model: OrderDetailDBModel = await self.create_order_detail_db_model(
                        order_detail=create_order_detail, product=product
                    )

                    product.stock -= order_detail_db_model.quantity

                    db_session.add(product)
                    db_session.add(order_db_model)
                    db_session.add(order_detail_db_model)

                    return order_detail_db_model.to_service_model()
                except IntegrityError as e:
                    self._handle_integrity_error(e)

    async def update_detail_with_product(
        self, order_detail_id: UUID, update_order_detail: UpdateOrderDetail
    ) -> OrderDetail:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                try:
                    query: Select = select(OrderDetailDBModel).filter(OrderDetailDBModel.id == order_detail_id)
                    result: ChunkedIteratorResult = await db_session.execute(query)
                    order_detail_db_model: OrderDetailDBModel = result.scalars().one()

                    old_product_name: str = order_detail_db_model.product_name
                    old_quantity: int = order_detail_db_model.quantity

                    # Update the old product stock
                    old_product_query: Select = select(ProductDBModel).filter(ProductDBModel.name == old_product_name)
                    old_product_result: ChunkedIteratorResult = await db_session.execute(old_product_query)
                    old_product: ProductDBModel = old_product_result.scalars().one()
                    old_product.stock += old_quantity

                    # Update the OrderDetail
                    order_detail_db_model.product_name = update_order_detail.product_name
                    order_detail_db_model.quantity = update_order_detail.quantity

                    # Update the new product stock
                    new_product_query = select(ProductDBModel).filter(
                        ProductDBModel.name == update_order_detail.product_name
                    )
                    new_product_result: ChunkedIteratorResult = await db_session.execute(new_product_query)
                    new_product: ProductDBModel = new_product_result.scalars().one()
                    new_product.stock -= update_order_detail.quantity

                    return order_detail_db_model.to_service_model()
                except NoResultFound as e:
                    self._handle_not_found_error(order_detail_id, e)

    def _handle_not_found_error(self, product_id, e):
        err_msg = f"No order detail found with id {product_id}."
        log.error(err_msg)
        raise ServiceException(message=err_msg, code=ErrorCode.NOT_FOUND) from e

    def _handle_integrity_error(self, e):
        if e.orig.pgcode == IntegrityErrorCode.UNIQUE_VIOLATION.value:
            raise ServiceException(
                message="Order detail already exists.",
                code=ErrorCode.DUPLICATE_ENTRY,
            ) from e
        raise e from e
