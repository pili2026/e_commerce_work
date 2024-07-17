import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import ChunkedIteratorResult, Select, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.future import select

from repository.model.user import UserDBModel
from repository.postgres_error_code.integrity_error_code import IntegrityErrorCode
from repository.role_permission import RolePermissionRepository
from service.model.role_permission import RolePermission
from service.model.user import CreateUser, UpdateUser, User
from util.app_error import ServiceException
from util.db_manager import DBManager


log = logging.getLogger(__name__)


class UserRepository:

    def __init__(self, db_manager: DBManager, role_permission_repository: RolePermissionRepository):
        self.db_manager = db_manager
        self.role_permission_repository = role_permission_repository

    async def get_user_list(self, user_id_list: Optional[UUID] = None) -> list[User]:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                query: Select = select(UserDBModel)

                if user_id_list:
                    query: Select = query.where(UserDBModel.id.in_(user_id_list))

                # TODO: Display permission
                result: ChunkedIteratorResult = await db_session.execute(query)
                user_list_db_model: list[UserDBModel] = result.scalars().all()

                user_list_model = []
                for user_db_model in user_list_db_model:
                    role_permission_list: list[RolePermission] = (
                        await self.role_permission_repository.get_role_permission_list(
                            db_session=db_session, role_list=[user_db_model.role]
                        )
                    )
                    user_list_model.append(user_db_model.to_service_model(role_permission_list))

                return user_list_model
                # return [user_db_model.to_service_model() for user_db_model in user_list_db_model]

    async def get_user(self, user_id: Optional[UUID] = None, account: Optional[str] = None) -> User:
        if not user_id and not account:
            raise ServiceException(
                code=400,
                message="At least one parameter (user_id, or account) must be provided",
            )

        async with self.db_manager.get_async_session() as db_session:
            try:
                query = select(UserDBModel)
                if user_id:
                    query = query.filter(UserDBModel.id == user_id)
                if account:
                    query = query.filter(UserDBModel.account == account)

                result = await db_session.execute(query)
                user_db_model: UserDBModel = result.scalars().one()
                return user_db_model.to_service_model()
            except NoResultFound as e:
                self._handle_not_found_error(user_id, e)

    async def insert_user(self, user: CreateUser) -> User:
        async with self.db_manager.get_async_session() as db_session:
            try:
                async with db_session.begin():
                    user_db_model = UserDBModel(
                        id=user.id,
                        account=user.account,
                        password=user.password.get_secret_value(),
                        role=user.role,
                        name=user.name,
                    )
                    db_session.add(user_db_model)
                    role_permission_list: list[RolePermission] = (
                        await self.role_permission_repository.get_role_permission_list(
                            db_session=db_session, role_list=[user_db_model.role]
                        )
                    )
                    return user_db_model.to_service_model(role_permission_list)
            except IntegrityError as e:
                self._handle_integrity_error(e)

    async def update_user(self, user_id: UUID, update_user: UpdateUser) -> User:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                try:
                    query = select(UserDBModel).filter(UserDBModel.id == user_id)
                    result = await db_session.execute(query)
                    user_db_model: UserDBModel = result.scalars().one()

                    user_db_model.name = update_user.name
                    user_db_model.role = update_user.role
                    return user_db_model.to_service_model()
                except NoResultFound as e:
                    self._handle_not_found_error(user_id, e)

    async def delete_user(self, user_id: UUID) -> bool:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                await db_session.execute(delete(UserDBModel).where(UserDBModel.id == user_id))
                return True

    def _handle_not_found_error(self, user_id, e):
        err_msg = f"No user found with id {user_id}."
        log.error(err_msg)
        raise ServiceException(message=err_msg, code=404) from e

    def _handle_integrity_error(self, e):
        if e.orig.pgcode == IntegrityErrorCode.UNIQUE_VIOLATION.value:
            raise ServiceException(
                message="User account already exists.",
                code=409,
            ) from e
        raise e from e
