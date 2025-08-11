from repository import TaskRepository, TaskCache
from schema import TaskResponse
from dataclasses import dataclass


@dataclass
class TaskService:

    task_repository : TaskRepository
    task_cache : TaskCache

    def get_tasks(self):
        cached_tasks = self.task_cache.get_tasks()

        if cached_tasks:
            return cached_tasks
        else:
            tasks = self.task_repository.get_all_tasks()
            tasks_schema = [TaskResponse.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema