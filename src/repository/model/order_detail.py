from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship
import uuid
from repository.model.base import DBModelBase
from service.model.order_detail import OrderDetail


class OrderDetailDBModel(DBModelBase):
    __tablename__ = "order_details"

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    order_id = Column(pgUUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(pgUUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product_name = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    order = relationship("OrderDBModel", passive_deletes=True, back_populates="details")
    product = relationship("ProductDBModel", passive_deletes=True, back_populates="order_details")

    def to_service_model(self) -> OrderDetail:
        return OrderDetail(
            id=self.id,
            order_id=self.order_id,
            product_id=self.product_id,
            product_name=self.product_name,
            product_price=self.product_price,
            quantity=self.quantity,
            total_price=self.total_price,
        )
