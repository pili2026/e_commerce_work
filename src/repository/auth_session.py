import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.future import select

from repository.model.auth_session import AuthSessionDBModel
from repository.postgres_error_code.integrity_error_code import IntegrityErrorCode
from service.model.auth_session import AuthSession, UpdateAuthSession
from util.app_error import ServiceException, ErrorCode
from util.db_manager import DBManager


log = logging.getLogger(__name__)


class AuthSessionRepository:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    async def get_auth_session(self, auth_session_id: UUID) -> AuthSession:
        async with self.db_manager.get_async_session() as db_session:
            try:
                query = select(AuthSessionDBModel).filter(AuthSessionDBModel.id == auth_session_id)
                result = await db_session.execute(query)
                auth_session_db_model: AuthSessionDBModel = result.scalars().one()
                return auth_session_db_model.to_service_model()
            except NoResultFound as e:
                self._handle_not_found_error(auth_session_id, e)

    async def insert_auth_session(self, auth_session: AuthSession) -> AuthSession:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                auth_session_db_model = AuthSessionDBModel(
                    id=auth_session.id,
                    user_id=auth_session.user_id,
                    issue_at=auth_session.issue_at,
                    access_token=auth_session.access_token,
                    access_token_expire_at=auth_session.access_token_expire_at,
                    refresh_token=auth_session.refresh_token,
                    refresh_token_expire_at=auth_session.refresh_token_expire_at,
                )

                try:
                    db_session.add(auth_session_db_model)
                    return auth_session_db_model.to_service_model()
                except IntegrityError as e:
                    self._handle_integrity_error(e)

    async def update_auth_session(self, auth_session_id: UUID, auth_session: UpdateAuthSession) -> AuthSession:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                try:
                    query = select(AuthSessionDBModel).filter(AuthSessionDBModel.id == auth_session_id)
                    result = await db_session.execute(query)
                    auth_session_db_model: AuthSessionDBModel = result.scalars().one()

                    auth_session_db_model.issue_at = auth_session.issue_at
                    auth_session_db_model.access_token = auth_session.access_token
                    auth_session_db_model.access_token_expire_at = auth_session.access_token_expire_at
                    auth_session_db_model.refresh_token = auth_session.refresh_token
                    auth_session_db_model.refresh_token_expire_at = auth_session.refresh_token_expire_at

                    return auth_session_db_model.to_service_model()
                except NoResultFound as e:
                    self._handle_not_found_error(auth_session_id, e)

    async def delete_auth_session(self, auth_session_id: UUID) -> bool:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                await db_session.execute(delete(AuthSessionDBModel).where(AuthSessionDBModel.id == auth_session_id))
                return True

    async def clear_ghost_auth_session(self) -> bool:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                await db_session.execute(
                    delete(AuthSessionDBModel).where(AuthSessionDBModel.refresh_token_expire_at < datetime.now())
                )
                return True

    def _handle_not_found_error(self, auth_session_id, e):
        err_msg = f"No auth_session found with id {auth_session_id}"
        log.error(err_msg)
        raise ServiceException(message=err_msg, code=ErrorCode.NOT_FOUND) from e

    def _handle_integrity_error(self, e):
        if e.orig.pgcode == IntegrityErrorCode.UNIQUE_VIOLATION.value:
            raise ServiceException(
                message="The auth_session already exists.",
                code=ErrorCode.DUPLICATE_ENTRY,
            ) from e
        raise e from e
