from dataclasses import dataclass
from schema import UserLoginSchema


@dataclass
class UserService:

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        pass