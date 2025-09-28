from uuid import UUID
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert
from dataclasses import dataclass

from models import UserProfile
from schema import UserCreateSchema
from database import AsyncSessionFactory


@dataclass
class UserRepository:
    """Repository for database operations related to users."""

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
        """Добавить пользователя и вернуть объект UserProfile с присвоенным ID"""
        async with self._session_scope() as session:
            query = (
                insert(UserProfile)
                .values(**user.model_dump(exclude_none=True))
                .returning(UserProfile.user_id)
            )
            result = await session.execute(query)
            user_id: UUID = result.scalar_one()

            stmt = select(UserProfile).where(UserProfile.user_id == user_id)
            user_model = (await session.execute(stmt)).scalar_one()
            return user_model

    async def get_user_by_id(self, user_id: UUID) -> UserProfile | None:
        async with self._session_scope() as session:
            stmt = select(UserProfile).where(UserProfile.user_id == user_id)
            return (await session.scalars(stmt)).one_or_none()

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        async with self._session_scope() as session:
            stmt = select(UserProfile).where(UserProfile.username == username)
            return (await session.scalars(stmt)).one_or_none()

    async def get_google_user(self, google_token: str) -> UserProfile | None:
        async with self._session_scope() as session:
            stmt = select(UserProfile).where(
                UserProfile.google_access_token == google_token
            )
            return (await session.scalars(stmt)).one_or_none()
