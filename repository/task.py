from contextlib import contextmanager
from uuid import UUID
from sqlalchemy import select, update, delete
from typing import Any, Optional
from sqlalchemy.orm import Session
from database import get_db_session
from schema import TaskCreate, TaskUpdate
from models import Task, Category


class TaskRepository:
    """Repository for database operations related to tasks."""

    def __init__(self):
        self.session_factory = get_db_session()

    @contextmanager
    def _session_scope(self) -> Session:
        """Context manager for handling database sessions.

        Provides automatic transaction management with commit/rollback
        and proper session cleanup.
        """
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

    def _get_task(self, *filters: Any) -> Optional[Task]:
        """Generic method to retrieve a single task matching given filters.

        Args:
            *filters: SQLAlchemy filter conditions

        Returns:
            Optional[Task]: Task object if found, None otherwise
        """
        with self._session_scope() as session:
            stmt = select(Task).where(*filters)
            return session.scalars(stmt).one_or_none()

    def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        """Retrieve a task by its unique identifier.

        Args:
            task_id: UUID of the task to find

        Returns:
            Optional[Task]: Task object if found, None otherwise
        """
        return self._get_task(Task.task_id == task_id)

    def get_task_by_name(self, name: str) -> Optional[Task]:
        """Retrieve a task by its name.

        Args:
            name: Name of the task to find

        Returns:
            Optional[Task]: Task object if found, None otherwise
        """
        return self._get_task(Task.name == name)

    def get_user_task(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Retrieve a specific task belonging to a particular user.

        Args:
            task_id: UUID of the task to find
            user_id: UUID of the task owner

        Returns:
            Optional[Task]: Task object if found and belongs to user, None otherwise
        """
        return self._get_task(Task.task_id == task_id, Task.user_id == user_id)

    def get_tasks_by_category(self, category_name: str) -> list[Task]:
        """Retrieve all tasks belonging to a specific category.

        Args:
            category_name: Name of the category to filter by

        Returns:
            list[Task]: List of tasks in the specified category
        """
        with self._session_scope() as session:
            stmt = (
                select(Task)
                .join(Category, Task.category_id == Category.category_id)
                .where(Category.name == category_name)
            )
            return session.scalars(stmt).all()

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks from the database.

        Returns:
            list[Task]: List of all tasks
        """
        with self._session_scope() as session:
            return session.scalars(select(Task)).all()

    def create_task(self, task: TaskCreate, user_id: UUID) -> UUID:
        """Retrieve all tasks from the database.

        Returns:
            list[Task]: List of all tasks
        """
        with self._session_scope() as session:
            task_model = Task(
                name=task.name,
                pomodoro_count=task.pomodoro_count,
                category_id=task.category_id,
                user_id=user_id,
            )
            session.add(task_model)
            session.flush()
            return task_model.task_id

    def delete_task(self, task_id: UUID, user_id: UUID) -> None:
        """Retrieve all tasks from the database.

        Returns:
            list[Task]: List of all tasks
        """
        with self._session_scope() as session:
            stmt = delete(Task).where(Task.task_id == task_id, Task.user_id == user_id)
            session.execute(stmt)

    def update_task(self, task_update: TaskUpdate) -> Task:
        """Retrieve all tasks from the database.

        Returns:
            list[Task]: List of all tasks
        """
        with self._session_scope() as session:
            stmt = (
                update(Task)
                .where(Task.task_id == task_update.task_id)
                .values(
                    name=task_update.name,
                    category_id=task_update.category_id,
                    pomodoro_count=task_update.pomodoro_count,
                )
                .returning(Task)
            )
            return session.scalars(stmt).one_or_none()
