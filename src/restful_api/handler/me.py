from fastapi import APIRouter, Depends, Request
from restful_api.schema.user import User as UserSchema
from service.authentication import PayloadField
from service.user import UserService
from util.authentication import get_current_user
from util.dependency_injector import get_user_service

me_router = APIRouter()


@me_router.get("/me", response_model=UserSchema)
async def get_me(
    request: Request,
    user_service: UserService = Depends(get_user_service),
    _: dict = Depends(get_current_user),
):
    user_id = request.state.token_payload[PayloadField.SUBJECT.value]
    user = await user_service.get_user_by_id(user_id=user_id)
    return user
