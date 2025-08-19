from contextlib import contextmanager
from uuid import UUID
from sqlalchemy import select, update
from typing import Any, Optional
from sqlalchemy.orm import Session
from database import get_db_session
from schema import TaskCreate, TaskUpdate
from models import Task, Category


class TaskRepository:

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

    def _get_task(self, *filters: Any) -> Optional[Task]:
        """Общий метод для выполнения запроса"""
        with self._session_scope() as session:
            stmt = select(Task).where(*filters)
            return session.scalars(stmt).one_or_none()

    def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        """Получить задачу по ID"""
        return self._get_task(Task.task_id == task_id)

    def get_task_by_name(self, name: str) -> Optional[Task]:
        """Получить задачу по имени"""
        return self._get_task(Task.name == name)

    def get_user_task(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        return self._get_task(Task.task_id == task_id, Task.user_id == user_id)

    def get_tasks_by_category(self, category_name: str) -> list[Task]:
        """Получить список задач по названию категории."""
        with self._session_scope() as session:
            stmt = (
                select(Task)
                .join(Category, Task.category_id == Category.category_id)
                .where(Category.name == category_name)
            )
            return session.scalars(stmt).all()

    def get_all_tasks(self) -> list[Task]:
        with self._session_scope() as session:
            return session.scalars(select(Task)).all()

    def create_task(self, task: TaskCreate, user_id: UUID) -> UUID:
        """Добавить задачу и вернуть объект Task с присвоенным ID"""
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

    def delete_task(self, task_id: UUID) -> None:
        """Удалить задачу"""
        with self._session_scope() as session:
            task: Task = self.get_task_by_id(task_id)
            if task is None:
                raise ValueError(f"Задача с ID {task_id} не найдена")
            session.delete(task)

    def update_task(self, task_update: TaskUpdate) -> Task:
        """Обновляет задачу по ID"""
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
