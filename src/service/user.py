from typing import Optional
from uuid import UUID

from pydantic import SecretStr

from repository.user import UserRepository
from service.authentication import AuthenticationService
from service.model.user import CreateUser, UpdateUser, User


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: UUID) -> User:
        user: User = await self.user_repository.get_user(user_id=user_id)
        return user

    async def get_user_by_account(self, account: str) -> User:
        user: User = await self.user_repository.get_user(account=account)
        return user

    async def get_user_list(self, user_id_list: Optional[list[UUID]] = None) -> list[User]:
        user_list: list[User] = await self.user_repository.get_user_list(user_id_list)
        return user_list

    async def create_user(self, create_user: CreateUser) -> User:
        password = create_user.password.get_secret_value()
        hashed_password = AuthenticationService.hash_password(password)

        create_user.password = SecretStr(hashed_password)
        created_user: User = await self.user_repository.insert_user(create_user)
        return created_user

    async def update_user(self, user_id: UUID, update_user: UpdateUser) -> User:
        updated_user: User = await self.user_repository.update_user(user_id, update_user)
        return updated_user

    async def delete_user(self, user_id: UUID) -> bool:
        result = await self.user_repository.delete_user(user_id)
        return result
