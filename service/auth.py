from dataclasses import dataclass

from exception import UserNotFoundException, UserUnCorrectPasswordException
from models import UserProfile
from schema import UserLoginSchema
from repository import UserRepository


@dataclass
class AuthService:
    user_repository: UserRepository

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_user(user=user, password=password)
        return UserLoginSchema(user_id=user.user_id, access_token=user.access_token)

    @staticmethod
    def _validate_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserUnCorrectPasswordException
