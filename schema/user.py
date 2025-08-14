from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str
