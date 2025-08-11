from repository import TaskRepository, TaskCache
from cache import get_redis_connection
from service import TaskService
from fastapi import Depends


def get_tasks_repository() -> TaskRepository:
    return TaskRepository()


def get_cache_tasks_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: TaskCache = Depends(get_cache_tasks_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache,
    )