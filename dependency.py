from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db_session
from repository import TaskRepository, TaskCache, UserRepository
from cache import get_redis_connection
from service import TaskService, UserService, AuthService
from settings import Settings


def get_tasks_repository() -> TaskRepository:
    return TaskRepository()


def get_cache_tasks_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


def get_task_service(
    task_repository: TaskRepository = Depends(get_tasks_repository),
    task_cache: TaskCache = Depends(get_cache_tasks_repository),
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache,
    )


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings())


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)
