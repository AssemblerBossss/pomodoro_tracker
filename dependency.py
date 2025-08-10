from repository import TaskRepository, TaskCache
from cache import get_redis_connection


def get_tasks_repository() -> TaskRepository:
    return TaskRepository()


def get_cache_tasks_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)
