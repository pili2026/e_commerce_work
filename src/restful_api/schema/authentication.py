from fastapi.security import OAuth2PasswordBearer
from service.model.base import BaseServiceModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


class AuthPayload(BaseServiceModel):
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str | None
