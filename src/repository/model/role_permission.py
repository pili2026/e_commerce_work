from sqlalchemy import Column, Enum
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship


from repository.model.base import DBModelBase
from service.model.permission import PermissionNamesEnum
from service.model.role import RoleNamesEnum
from service.model.role_permission import RolePermission


class RolePermissionDBModel(DBModelBase):
    __tablename__ = "role_permissions"

    id = Column(pgUUID(as_uuid=True), primary_key=True, nullable=False)
    role = Column(Enum(RoleNamesEnum, name="role_name_enum"), nullable=False)
    permission = Column(Enum(PermissionNamesEnum, name="permission_name_enum"), nullable=False)

    # users = relationship("UserDBModel", back_populates="role_permission")

    def to_service_model(self) -> RolePermission:
        return RolePermission(id=self.id, role=self.role, permission=self.permission)
