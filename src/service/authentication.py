import logging
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Optional, Tuple
from uuid import UUID, uuid4

import bcrypt
import jwt
from strawberry.types import Info

from repository.auth_session import AuthSessionRepository
from repository.model.base import get_utc_datetime_now_without_timezone
from repository.user import UserRepository
from service.model.auth_payload import AuthPayload
from service.model.auth_session import AuthSession, UpdateAuthSession
from service.model.user import User
from util.app_error import ServiceException, ErrorCode, ServiceException
from util.config_manager import ConfigManager


log = logging.getLogger(__name__)

TOKEN_TYPE = "Bearer"
ACCESS_TOKEN_LIFETIME = timedelta(hours=1)
REFRESH_TOKEN_LIFETIME = timedelta(days=30)


class PayloadField(StrEnum):
    SUBJECT = "sub"  # Subject, refer to user ID
    ISSUE_AT = "iat"  # Issue at
    EXPIRE_AT = "exp"  # Expire at
    SESSION_ID = "sid"  # Session ID


class AuthenticationService:

    def __init__(
        self,
        auth_session_repository: AuthSessionRepository,
        user_repository: UserRepository,
        config_manager: ConfigManager,
    ):
        self.auth_session_repository = auth_session_repository
        self.user_repository = user_repository
        self.config_manager = config_manager

    async def login(self, account: str, password: str) -> AuthPayload:
        try:
            user: User = await self.user_repository.get_user(account=account)
        except ServiceException:
            self.__raise_invalid_credentials_error()

        if not self.__is_password_correct(plain=password, hashed=user.password.get_secret_value()):
            self.__raise_invalid_credentials_error()

        auth_session = await self._create_auth_session(user.id)
        auth_payload = self.__make_auth_payload(auth_session)

        return auth_payload

    async def logout(self, session_id: UUID) -> bool:
        result = await self.auth_session_repository.delete_auth_session(session_id)
        return result

    async def refresh_token(self, access_token: str, refresh_token: str) -> AuthPayload:
        refresh_token_payload = self.get_jwt_token_payload(refresh_token)
        auth_session_id = refresh_token_payload[PayloadField.SESSION_ID.value]
        auth_session_user_id = refresh_token_payload[PayloadField.SUBJECT.value]

        try:
            auth_session = await self.auth_session_repository.get_auth_session(auth_session_id)
        except ServiceException:
            self.__raise_invalid_session_error()

        # Check access_token and refresh_token are matched.
        if auth_session.access_token != access_token:
            self.__raise_invalid_session_error()

        updated_auth_session = await self._renew_auth_session(auth_session_id, auth_session_user_id)
        auth_payload = self.__make_auth_payload(updated_auth_session)

        return auth_payload

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    async def access_token_exists(self, session_id: UUID, access_token: str) -> bool:
        try:
            auth_session: AuthSession = await self.auth_session_repository.get_auth_session(session_id)
            return auth_session.access_token == access_token
        except ServiceException:
            return False

    def get_header_authorization(self, info: Info) -> str:
        header_authorization = info.context.request.headers.get("Authorization")
        if header_authorization is None:
            self.__raise_invalid_session_error("Authorization header is missing.")

        return header_authorization

    def get_jwt_token(self, header_authorization: str) -> str:
        bearer_prefix = "Bearer "

        if not header_authorization.startswith(bearer_prefix):
            self.__raise_invalid_format_error()

        jwt_token = header_authorization[len(bearer_prefix) :]
        return jwt_token

    def get_jwt_token_payload(self, token: str) -> dict:
        secret_key: str = self.config_manager.get_config()["SECRET_KEY"]
        algorithm: str = self.config_manager.get_config()["JWT_ALGORITHM"]

        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        except jwt.ExpiredSignatureError:
            self.__raise_session_expired_error()
        except jwt.InvalidTokenError:
            self.__raise_invalid_session_error()

        return payload

    def _create_jwt_token(
        self, user_id: UUID, issue_at: datetime, lifetime: timedelta, session_id: UUID
    ) -> Tuple[str, datetime]:
        payload = {
            PayloadField.SUBJECT.value: str(user_id),
            PayloadField.ISSUE_AT.value: issue_at,
            PayloadField.EXPIRE_AT.value: issue_at + lifetime,
            PayloadField.SESSION_ID.value: str(session_id),
        }
        secret_key = self.config_manager.get_config()["SECRET_KEY"]
        algorithm = self.config_manager.get_config()["JWT_ALGORITHM"]

        jwt_token: str = jwt.encode(payload, secret_key, algorithm=algorithm)
        return jwt_token, payload[PayloadField.EXPIRE_AT.value]

    async def _create_auth_session(self, user_id: UUID) -> AuthSession:
        session_id = uuid4()
        issue_at = get_utc_datetime_now_without_timezone()
        access_token, access_token_expire_at = self._create_jwt_token(
            user_id, issue_at, ACCESS_TOKEN_LIFETIME, session_id
        )
        refresh_token, refresh_token_expire_at = self._create_jwt_token(
            user_id, issue_at, REFRESH_TOKEN_LIFETIME, session_id
        )

        auth_session: AuthSession = AuthSession(
            id=session_id,
            user_id=user_id,
            issue_at=issue_at,
            access_token=access_token,
            access_token_expire_at=access_token_expire_at,
            refresh_token=refresh_token,
            refresh_token_expire_at=refresh_token_expire_at,
        )
        created_auth_session = await self.auth_session_repository.insert_auth_session(auth_session)

        return created_auth_session

    async def _renew_auth_session(self, session_id: UUID, user_id: UUID) -> AuthSession:
        issue_at = get_utc_datetime_now_without_timezone()
        access_token, access_token_expire_at = self._create_jwt_token(
            user_id, issue_at, ACCESS_TOKEN_LIFETIME, session_id
        )
        refresh_token, refresh_token_expire_at = self._create_jwt_token(
            user_id, issue_at, REFRESH_TOKEN_LIFETIME, session_id
        )

        update_auth_session = UpdateAuthSession(
            issue_at=issue_at,
            access_token=access_token,
            access_token_expire_at=access_token_expire_at,
            refresh_token=refresh_token,
            refresh_token_expire_at=refresh_token_expire_at,
        )

        try:
            updated_auth_session = await self.auth_session_repository.update_auth_session(
                session_id, update_auth_session
            )

            return updated_auth_session
        except ServiceException:
            self.__raise_invalid_session_error()

    def __is_password_correct(self, plain: str, hashed: str) -> bool:
        plain_password_bytes = plain.encode("utf-8")
        hashed_password_bytes = hashed.encode("utf-8")
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

    def __make_auth_payload(self, auth_session: AuthSession) -> AuthPayload:
        return AuthPayload(
            token_type=TOKEN_TYPE,
            access_token=auth_session.access_token,
            expires_in=int(ACCESS_TOKEN_LIFETIME.total_seconds()),
            refresh_token=auth_session.refresh_token,
        )

    def __raise_invalid_credentials_error(self, message: Optional[str] = "Account not found or incorrect password."):
        raise ServiceException(message=message, code=ErrorCode.INVALID_CREDENTIALS)

    def __raise_invalid_format_error(self, message: Optional[str] = "Token validation failed: invalid format"):
        raise ServiceException(message=message, code=ErrorCode.INVALID_FORMAT)

    def __raise_invalid_session_error(self, message: Optional[str] = "Token validation failed: invalid session"):
        raise ServiceException(message=message, code=ErrorCode.INVALID_SESSION)

    def __raise_session_expired_error(self, message: Optional[str] = "Token validation failed: session expired"):
        raise ServiceException(message=message, code=ErrorCode.SESSION_EXPIRED)
