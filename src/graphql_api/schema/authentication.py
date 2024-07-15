import strawberry


@strawberry.type
class AuthPayload:
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str | None
