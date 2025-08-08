from repository import TaskRepository


def get_tasks_repository() -> TaskRepository:
    return TaskRepository()