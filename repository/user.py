from dataclasses import dataclass


@dataclass
class UserRepository:

    def create_user(self, username: str, password: str) -> User:
        pass