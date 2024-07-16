from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship

from repository.model.base import DBModelBase
from service.model.role import RoleNamesEnum
from service.model.user import User


class UserDBModel(DBModelBase):
    __tablename__ = "users"

    id = Column(pgUUID(as_uuid=True), primary_key=True, nullable=False)
    account = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    role = Column(Enum(RoleNamesEnum, name="role_name_enum"), nullable=False)

    role_permission = relationship("RolePermissionDBModel", back_populates="users")
    sessions = relationship("AuthSessionDBModel", cascade="all, delete", back_populates="user")
    orders = relationship("OrderDBModel", back_populates="user")

    def to_service_model(self) -> User:
        return User(id=self.id, account=self.account, password=self.password, name=self.name, role=self.role)
