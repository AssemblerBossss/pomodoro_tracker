from typing import Annotated
from fastapi import APIRouter, status, Depends

from dependency import get_user_service
from schema import UserLoginSchema, UserCreateSchema
from service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
async def create_user(
        user: UserCreateSchema,
        user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserLoginSchema:
    return user_service.create_user(user.username, user.password)
