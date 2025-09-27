from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserLoginSchema(BaseModel):
    user_id: UUID
    access_token: str


class UserCreateSchema(BaseModel):
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    google_access_token: str | None = None
    yandex_access_token: str | None = None
    name: str | None = None