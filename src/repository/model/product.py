from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship

from repository.model.base import DBModelBase
from service.model.product import Product


class ProductDBModel(DBModelBase):
    __tablename__ = "products"

    id = Column(pgUUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    order_details = relationship("OrderDetailDBModel", passive_deletes=True, back_populates="product")

    def to_service_model(self) -> Product:
        return Product(id=self.id, name=self.name, price=self.price, stock=self.stock)
