from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from repository.model.base import DBModelBase
from service.model.order import Order, OrderStatusEnum


class OrderDBModel(DBModelBase):
    __tablename__ = "orders"

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(pgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(OrderStatusEnum, name="order_status_enum"), nullable=False)

    user = relationship("UserDBModel", passive_deletes=True, back_populates="orders")
    details = relationship("OrderDetailDBModel", passive_deletes=True, back_populates="order")

    def to_service_model(self) -> Order:
        return Order(
            id=self.id,
            user_id=self.user_id,
            status=self.status,
            # details=[detail.to_service_model() for detail in self.details],
        )
