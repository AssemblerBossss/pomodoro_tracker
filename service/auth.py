from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID
from jose import jwt, JWTError, ExpiredSignatureError

from exception import (
    UserNotFoundException,
    UserUnCorrectPasswordException,
    TokenExpiredException,
    InvalidTokenException,
)
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema
from settings import Settings


@dataclass
class AuthService:
    """Service for handling user authentication and JWT token generation.

    Attributes:
        user_repository: Repository for user data access
        settings: Application settings containing JWT configuration
    """

    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        """Authenticate user and return access token.

        Args:
            username: User's login name
            password: User's plaintext password

        Returns:
            UserLoginSchema with user_id and JWT token

        Raises:
            UserNotFoundException: If user doesn't exist
            UserUnCorrectPasswordException: If password doesn't match
        """
        user = self.user_repository.get_user_by_username(username)
        self._validate_user(user=user, password=password)
        access_token = self.generate_access_token(user_id=user.user_id)
        return UserLoginSchema(user_id=user.user_id, access_token=access_token)

    def generate_access_token(self, user_id: UUID) -> str:
        """Generate JWT token for authenticated user.

        Args:
            user_id: UUID of authenticated user

        Returns:
            Signed JWT token with user_id and expiration claim
        """
        expires_date_unix = (datetime.utcnow() + timedelta(days=7)).timestamp()

        encode = {
            "user_id": str(user_id),
            "exp": expires_date_unix,
        }

        return jwt.encode(
            encode, self.settings.JWT_SECRET, algorithm=self.settings.JWT_ALGORITHM
        )

    def get_user_id_from_access_token(self, access_token: str) -> UUID:
        try:
            payload = jwt.decode(
                token=access_token,
                key=self.settings.JWT_SECRET,
                algorithms=self.settings.JWT_ALGORITHM,
                options={"verify_exp": True},
            )
            return UUID(payload["user_id"])
        except ExpiredSignatureError:
            raise TokenExpiredException
        except JWTError:
            raise InvalidTokenException

    @staticmethod
    def _validate_user(user: UserProfile, password: str) -> None:
        """Validate user credentials.

        Args:
            user: UserProfile object or None
            password: Plaintext password to verify

        Raises:
            UserNotFoundException: If user is None
            UserUnCorrectPasswordException: If password doesn't match
        """
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserUnCorrectPasswordException
