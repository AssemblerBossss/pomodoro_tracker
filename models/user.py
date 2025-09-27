from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from models.tasks import Base


class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    username: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    google_access_token: Mapped[Optional[str]]
    yandex_access_token: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
