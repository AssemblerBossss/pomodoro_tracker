from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from uuid import uuid4


Base = declarative_base()


class Category(Base):
    __tablename__ = "Categories"

    category_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(unique=True)

    # Исправлено: tasks (маленькая буква) - имя атрибута
    tasks: Mapped[list["Task"]] = relationship(back_populates="category")


class Task(Base):
    __tablename__ = "Tasks"

    task_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(255))
    pomodoro_count: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("Categories.category_id"),
        nullable=True,  # Это ключевое изменение
    )

    # Исправлено: category (маленькая буква) - имя атрибута
    category: Mapped["Category"] = relationship(back_populates="tasks")
