from service.model.base import BaseServiceModel
from service.model.permission import PermissionNamesEnum
from service.model.role import RoleNamesEnum


class AuthPayload(BaseServiceModel):
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str
