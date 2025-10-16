from uuid import UUID
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert
from typing import Any, Optional

from models import UserProfile
from schema import UserCreateSchema
from database import AsyncSessionFactory


class UserRepository:
    """Repository for database operations related to users.

    Provides asynchronous methods for user data access and management
    using SQLAlchemy AsyncSession for database operations.
    """

    def __init__(self):
        self.session_factory = AsyncSessionFactory

    @asynccontextmanager
    async def _session_scope(self) -> AsyncSession:
        """Context manager for handling database sessions.

        Provides automatic transaction management with commit/rollback
        and proper session cleanup.
        """
        async with self.session_factory() as session:
            try:
                session.expire_on_commit = False
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def create_user(self, user: UserCreateSchema) -> UserProfile:
        """Create a new user in the database.
        Args:
            user: UserCreateSchema containing user data for creation

        Returns:
            UserProfile: Created user object with assigned user_id

        Raises:
            SQLAlchemyError: If database operation fails
        """
        # async with self._session_scope() as session:
        #     query = (
        #         insert(UserProfile)
        #         .values(**user.model_dump(exclude_none=True))
        #         .returning(UserProfile.user_id)
        #     )
        #     result = await session.execute(query)
        #     user_id: UUID = result.scalar_one()
        #
        #     user_model = await self.get_user_by_id(user_id=user_id)
        #     return user_model
        async with self._session_scope() as session:
            try:
                user_data = user.model_dump(exclude_none=True)
                stmt = (
                    insert(UserProfile)
                    .values(**user_data)
                    .returning(UserProfile)
                )

                result = await session.execute(stmt)
                user_model = result.scalar_one()

                print(f"Created user with ID: {user_model.user_id}")
                return user_model

            except Exception as e:
                print(f"Error creating user: {e}")
                raise

    async def _get_user(self, *filters: Any) -> Optional[UserProfile]:
        """Internal method to retrieve a single user matching given filters.

        Args:
            *filters: SQLAlchemy filter conditions to apply to the query

        Returns:
            Optional[UserProfile]: User object if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        async with self._session_scope() as session:
            stmt = select(UserProfile).where(*filters)
            return (await session.scalars(stmt)).one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> Optional[UserProfile]:
        """Retrieve user by their unique identifier"""
        return await self._get_user(UserProfile.user_id == user_id)

    async def get_user_by_username(self, username: str) -> Optional[UserProfile]:
        """Retrieve user by username."""
        return await self._get_user(UserProfile.username == username)

    async def get_user_by_email(self, email: str) -> Optional[UserProfile]:
        """Retrieve user by email address."""
        return await self._get_user(UserProfile.email == email)

    async def get_google_user(self, google_token: str) -> Optional[UserProfile]:
        """Retrieve user by Google OAuth access token."""
        return await self._get_user(UserProfile.google_access_token == google_token)