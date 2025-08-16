from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select, update
from dataclasses import dataclass
from contextlib import contextmanager

from models import UserProfile
from database import get_db_session


@dataclass
class UserRepository:

    def __init__(self):
        self.session_factory = get_db_session()

    @contextmanager
    def _session_scope(self) -> Session:
        """Контекстный менеджер для управления сессией"""
        session = self.session_factory()
        session.expire_on_commit = False
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_user(self, username: str, password: str) -> UserProfile:
        """Добавить пользователя и вернуть объект UserProfile с присвоенным ID"""
        with self._session_scope() as session:
            user_model = UserProfile(
                user_name=username, password=password
            )
            session.add(user_model)
            session.flush()  # Получаем ID без коммита
            return user_model  #

    def get_user_by_id(self, user_id: UUID) -> UserProfile | None:
        with self._session_scope() as session:
            stmt = select(UserProfile).where(UserProfile.user_id == user_id)
            return session.scalars(stmt).one_or_none()

    def get_user_by_username(self, username: str) -> UserProfile | None:
        with self._session_scope() as session:
            stmt = select(UserProfile).where(UserProfile.user_name == username)
            return session.scalars(stmt).one_or_none()