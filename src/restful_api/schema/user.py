from typing import Optional
from uuid import UUID

from pydantic import Field, field_validator

from service.model.base import BaseServiceModel
from service.model.role import RoleNamesEnum
from service.model.role_permission import RolePermission as RolePermissionModel
from util.validation_utils import validate_input_length


class User(BaseServiceModel):
    id: UUID
    account: str
    name: Optional[str]
    role: RoleNamesEnum
    role_permission_list: list[RolePermissionModel]


class CreateUserInput(BaseServiceModel):
    account: str = Field(..., min_length=1, max_length=20)
    name: Optional[str] = Field(None, min_length=0, max_length=20)
    password: str = Field(..., min_length=1, max_length=50)
    role: RoleNamesEnum

    @field_validator("account", "password")
    def validate_non_empty(cls, v):
        if not v:
            raise ValueError("must not be empty")
        return v

    class Config:
        use_enum_values = True


class UpdateUserInput(BaseServiceModel):
    name: str
    role: RoleNamesEnum
