from typing import Annotated, Optional
from uuid import UUID

from pydantic import Field, SecretStr

from service.model.base import AUTO_GEN_UUID4_FIELD, NAME_FIELD, BaseServiceModel
from service.model.role import RoleNamesEnum


ACCOUNT_FIELD = Field(min_length=1, max_length=20)
LimitedSecretStr = Annotated[SecretStr, Field(min_length=1, max_length=30)]


class User(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    account: str = ACCOUNT_FIELD
    password: SecretStr
    name: Optional[str] = NAME_FIELD
    role: RoleNamesEnum


class CreateUser(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    account: str = ACCOUNT_FIELD
    password: LimitedSecretStr
    name: Optional[str] = NAME_FIELD
    role: RoleNamesEnum


class UpdateUser(BaseServiceModel):
    name: Optional[str] = NAME_FIELD
    role: RoleNamesEnum
