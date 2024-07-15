from service.model.base import BaseServiceModel


class AuthPayload(BaseServiceModel):
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str
