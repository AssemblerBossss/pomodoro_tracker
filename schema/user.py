from uuid import UUID
from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    user_id: UUID
    access_token: str


class UserCreateSchema(BaseModel):
    username: str
    password: str
