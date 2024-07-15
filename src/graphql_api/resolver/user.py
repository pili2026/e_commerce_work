from typing import Optional
from uuid import UUID

import strawberry
from strawberry.types import Info

from graphql_api.decorator.authentication import validate_jwt_token
from graphql_api.schema.user import CreateUserInput, UpdateUserInput
from graphql_api.schema.user import User as UserSchema
from service.authentication import PayloadField
from service.model.user import CreateUser, UpdateUser, User
from service.user import UserService


@strawberry.type
class UserQuery:
    @strawberry.field
    @validate_jwt_token
    async def get_user_list(self, info: Info, user_id_list: Optional[list[UUID]] = None) -> Optional[list[UserSchema]]:
        user_service: UserService = info.context.user_service
        user_list: list[User] = await user_service.get_user_list(user_id_list=user_id_list)
        return user_list

    @strawberry.field
    @validate_jwt_token
    async def get_user(self, info: Info, user_id: UUID = None) -> Optional[UserSchema]:
        user_service: UserService = info.context.user_service
        user: User = await user_service.get_user_by_id(user_id=user_id)
        return user

    @strawberry.field
    @validate_jwt_token
    async def get_me(self, info: Info) -> Optional[UserSchema]:
        token_payload: dict = info.context.token_payload
        user_id = token_payload[PayloadField.SUBJECT.value]

        user_service: UserService = info.context.user_service
        user: User = await user_service.get_user_by_id(user_id=user_id)
        return user


@strawberry.type
class UserMutation:
    @strawberry.mutation
    @validate_jwt_token
    async def create_user(self, info: Info, user: CreateUserInput) -> UserSchema:
        user_service: UserService = info.context.user_service
        create_user_model = CreateUser(
            account=user.account,
            password=user.password,
            name=user.name,
            role=user.role,
        )
        created_user: User = await user_service.create_user(create_user=create_user_model)
        return created_user

    @strawberry.mutation
    @validate_jwt_token
    async def update_user(self, info: Info, user_id: UUID, user: UpdateUserInput) -> UserSchema:
        user_service: UserService = info.context.user_service

        update_user_model = UpdateUser(name=user.name, role=user.role)
        updated_user: User = await user_service.update_user(user_id=user_id, update_user=update_user_model)
        return updated_user

    @strawberry.mutation
    @validate_jwt_token
    async def delete_user(self, info: Info, user_id: UUID) -> bool:
        user_service: UserService = info.context.user_service
        result = await user_service.delete_user(user_id=user_id)
        return result
