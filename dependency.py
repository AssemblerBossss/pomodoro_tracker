from repository import TaskRepository
from repository.cache_tasks import CacheTasks


def get_tasks_repository() -> TaskRepository:
    return TaskRepository()


def get_cache_tasks_repository() -> CacheTasks: