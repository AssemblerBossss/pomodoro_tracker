from dataclasses import dataclass

from schema import UserLoginSchema
from repository import UserRepository


@dataclass
class AuthService:
    pass
    # user_repository: UserRepository
    #
    # def create_user(self, username: str, password: str) -> UserLoginSchema:
    #     user = self.user_repository.create_user(username, password)
    #     return UserLoginSchema(user_id=user.user_id, access_token=user.access_token)
