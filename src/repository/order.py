import logging
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import ChunkedIteratorResult, Select, delete, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import selectinload

from repository.model.order import OrderDBModel
from repository.postgres_error_code.integrity_error_code import IntegrityErrorCode
from service.model.order import CreateOrder, Order
from util.app_error import AppError, ErrorCode
from util.db_manager import DBManager


log = logging.getLogger(__name__)


class OrderRepository:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    async def get_order_list(self, order_id_list: Optional[UUID] = None) -> list[Order]:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                query: Select = select(OrderDBModel).options(selectinload(OrderDBModel.detail))

                if order_id_list:
                    query: Select = query.where(Order.id.in_(order_id_list))

                result: ChunkedIteratorResult = await db_session.execute(query)
                order_db_model_list: list[OrderDBModel] = result.scalars().all()

                return [order_db_model.to_service_model() for order_db_model in order_db_model_list]

    async def get_order(self, order_id: Optional[UUID] = None, user_id: Optional[UUID] = None) -> Order:
        if not order_id:
            raise HTTPException(
                code=ErrorCode.INVALID_FORMAT,
                message="The order_id is required",
            )

        async with self.db_manager.get_async_session() as db_session:
            try:
                query: Select = select(OrderDBModel)
                if order_id:
                    query: Select = query.filter(OrderDBModel.id == order_id)
                if user_id:
                    query: Select = query.filter(OrderDBModel.user_id == user_id)

                result: ChunkedIteratorResult = await db_session.execute(query)
                order_db_model: OrderDBModel = result.scalars().one()
                return order_db_model.to_service_model()
            except NoResultFound as e:
                self._handle_not_found_error(order_id, e)

    async def create_order_db_model(self, order: CreateOrder) -> OrderDBModel:
        try:
            order_db_model = OrderDBModel(id=order.id, user_id=order.user_id, status=order.status)
            return order_db_model
        except IntegrityError as e:
            self._handle_integrity_error(e)

    def _handle_not_found_error(self, order_id, e):
        err_msg = f"No order found with id {order_id}."
        log.error(err_msg)
        raise AppError(message=err_msg, code=ErrorCode.NOT_FOUND) from e

    def _handle_integrity_error(self, e):
        if e.orig.pgcode == IntegrityErrorCode.UNIQUE_VIOLATION.value:
            raise AppError(
                message="Order already exists.",
                code=ErrorCode.DUPLICATE_ENTRY,
            ) from e
        raise e from e
