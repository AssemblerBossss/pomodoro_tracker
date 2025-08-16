from dataclasses import dataclass
from uuid import UUID
from jose import jwt
import datetime as dt
from datetime import timedelta

from exception import UserNotFoundException, UserUnCorrectPasswordException
from models import UserProfile
from schema import UserLoginSchema
from repository import UserRepository
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_user(user=user, password=password)
        access_token = self.generate_access_token(user_id=user.user_id)
        return UserLoginSchema(user_id=user.user_id, access_token=access_token)

    def generate_access_token(self, user_id: UUID) -> str:
        expires_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
        encode = {
            "user_id": str(user_id),
            "expire": expires_date_unix,
        }

        token = jwt.encode(
            encode, self.settings.JWT_SECRET, algorithm=self.settings.JWT_ALGORITHM
        )
        return token

    @staticmethod
    def _validate_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserUnCorrectPasswordException
