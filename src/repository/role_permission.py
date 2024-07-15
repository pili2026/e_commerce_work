import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import ChunkedIteratorResult, Select
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.future import select

from repository.model.role_permission import RolePermissionDBModel
from repository.postgres_error_code.integrity_error_code import IntegrityErrorCode
from service.model.role import RoleNamesEnum
from service.model.role_permission import PermissionNamesEnum, RolePermission, UpdateRolePermission
from util.app_error import AppError, ErrorCode
from util.db_manager import DBManager


log = logging.getLogger(__name__)


class RolePermissionRepository:

    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    async def get_role_permission_list(self, role_list: list[RoleNamesEnum] = None) -> list[RolePermission]:
        async with self.db_manager.get_async_session() as db_session:
            query: Select = select(RolePermissionDBModel)
            if role_list:
                query = query.where(RolePermissionDBModel.role.in_(role_list))

            result: ChunkedIteratorResult = await db_session.execute(query)
            role_permissions_db_model: list[RolePermissionDBModel] = result.scalars().all()
            return [role_permission.to_service_model() for role_permission in role_permissions_db_model]

    async def get_role_permission(
        self,
        role_permission_id: Optional[UUID] = None,
        role: Optional[RoleNamesEnum] = None,
        permission: Optional[PermissionNamesEnum] = None,
    ) -> RolePermission:
        if not role_permission_id and not role and not permission:
            raise AppError(
                code=ErrorCode.INVALID_FORMAT,
                message="At least one parameter (id, role, or permission) must be provided",
            )

        async with self.db_manager.get_async_session() as db_session:
            try:
                query = select(RolePermissionDBModel)
                if role_permission_id:
                    query = query.filter(RolePermissionDBModel.id == role_permission_id)
                if role:
                    query = query.filter(RolePermissionDBModel.role == role)
                if permission:
                    query = query.filter(RolePermissionDBModel.permission == permission)

                result = await db_session.execute(query)
                role_permission_db_model: RolePermissionDBModel = result.scalars().one()
                return role_permission_db_model.to_service_model()
            except NoResultFound as e:
                self._handle_not_found_error(role_permission_id, e)

            except MultipleResultsFound as e:
                self._handle_multiple_results_found_error(role_permission_id, e)

    async def insert_role_permission(self, role_permission: RolePermission) -> RolePermission:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                role_permission_db_model = RolePermissionDBModel(
                    id=role_permission.id, role=role_permission.role, permission=role_permission.permission
                )
                try:
                    db_session.add(role_permission_db_model)
                    return role_permission_db_model.to_service_model()
                except IntegrityError as e:
                    self._handle_integrity_error(role_permission, e)

    async def update_role_permission(
        self, role_permission_id: UUID, role_permission: UpdateRolePermission
    ) -> RolePermission:
        async with self.db_manager.get_async_session() as db_session:
            async with db_session.begin():
                try:
                    query = select(RolePermissionDBModel).where(RolePermissionDBModel.id == role_permission_id)
                    result = await db_session.execute(query)
                    role_permission_db_model: RolePermissionDBModel = result.scalars().one()

                    role_permission_db_model.role = role_permission.role
                    role_permission_db_model.permission = role_permission.permission
                    return role_permission_db_model.to_service_model()
                except NoResultFound as e:
                    self._handle_not_found_error(role_permission_id, e)

    def _handle_not_found_error(self, role_permission_id, e):
        err_msg = f"No role_permission found with id {role_permission_id}"
        log.error(err_msg)
        raise AppError(message=err_msg, code=ErrorCode.NOT_FOUND) from e

    def _handle_multiple_results_found_error(self, role_permission_id, e):
        err_msg = f"Multiple role_permissions found with id {role_permission_id}, which should be unique."
        log.error(err_msg)
        raise AppError(message=err_msg, code=ErrorCode.DUPLICATE_ENTRY) from e

    def _handle_integrity_error(self, role_permission, e):
        if e.orig.pgcode == IntegrityErrorCode.UNIQUE_VIOLATION.value:
            raise AppError(
                message=f"The id, {role_permission.id} already exists.",
                code=ErrorCode.DUPLICATE_ENTRY,
            ) from e
