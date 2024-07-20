from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Request, status

from restful_api.schema.user import (
    CreateUserInput as CreateUserInputSchema,
    UpdateUserInput as UpdateUserInputSchema,
    User as UserSchema,
)

from service.model.authentication import Payload
from service.model.user import CreateUser, UpdateUser, User
from service.user import UserService
from util.authentication import get_current_user
from util.dependency_injector import get_user_service


user_router = APIRouter()


@user_router.post("/user/list", response_model=list[UserSchema])
async def get_user_list(
    user_id_list: Optional[list[UUID]] = None,
    user_service: UserService = Depends(get_user_service),
    _: Payload = Depends(get_current_user),
):
    user_list: list[User] = await user_service.get_user_list(user_id_list=user_id_list)
    return user_list


@user_router.get("/user/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
    _: Payload = Depends(get_current_user),
):
    user = await user_service.get_user_by_id(user_id=user_id)
    return user


@user_router.post("/user", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: CreateUserInputSchema,
    user_service: UserService = Depends(get_user_service),
    _: Payload = Depends(get_current_user),
):
    create_user_model = CreateUser(
        account=user.account,
        password=user.password,
        name=user.name,
        role=user.role,
    )
    created_user: User = await user_service.create_user(create_user=create_user_model)
    return created_user


@user_router.put("/user/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: UUID,
    user: UpdateUserInputSchema,
    user_service: UserService = Depends(get_user_service),
    _: Payload = Depends(get_current_user),
):
    update_user_model = UpdateUser(name=user.name, role=user.role)
    updated_user: User = await user_service.update_user(user_id=user_id, update_user=update_user_model)
    return updated_user


@user_router.delete("/user/{user_id}", response_model=bool)
async def delete_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
    _: Payload = Depends(get_current_user),
):
    result: bool = await user_service.delete_user(user_id=user_id)
    return result
