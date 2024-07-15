from datetime import datetime
from uuid import UUID

from service.model.base import AUTO_GEN_UUID4_FIELD, BaseServiceModel


class AuthSession(BaseServiceModel):
    id: UUID = AUTO_GEN_UUID4_FIELD
    user_id: UUID
    issue_at: datetime
    access_token: str
    access_token_expire_at: datetime
    refresh_token: str
    refresh_token_expire_at: datetime


class UpdateAuthSession(BaseServiceModel):
    issue_at: datetime
    access_token: str
    access_token_expire_at: datetime
    refresh_token: str
    refresh_token_expire_at: datetime
