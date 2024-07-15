from uuid import uuid4

from pydantic import BaseModel, Field


class BaseServiceModel(BaseModel):
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__dict__ == other.__dict__


AUTO_GEN_UUID4_FIELD = Field(default_factory=uuid4)
NAME_FIELD = Field(default=None, min_length=0, max_length=20)
PRICE_FIELD = Field(default=0.0, ge=0.0, description="Price must be a non-negative value")
STOCK_FIELD = Field(default=0, ge=0, description="Stock must be a non-negative value")
