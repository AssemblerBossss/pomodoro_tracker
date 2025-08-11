from typing import List
from uuid import UUID
from repository import TaskRepository, TaskCache
from schema import TaskResponse, TaskCreate, TaskUpdate
from dataclasses import dataclass


@dataclass
class TaskService:
    """Service layer for task operations with Redis caching.

    Coordinates between task repository (database) and task cache (Redis).
    """

    task_repository: TaskRepository
    task_cache: TaskCache

    def get_tasks(self) -> List[TaskResponse]:
        """Retrieve all tasks from cache or database.

        Returns cached tasks if available, otherwise fetches from database,
        updates cache, and returns the results.

        Returns:
            List[TaskResponse]: List of all tasks
        """
        if cached := self.task_cache.get_tasks():
            return cached

        tasks = [
            TaskResponse.model_validate(t) for t in self.task_repository.get_all_tasks()
        ]
        self.task_cache.set_tasks(tasks)
        return tasks

    def create_task(self, task: TaskCreate) -> TaskResponse:
        """Create a new task and add it to cache.

        Args:
            task (TaskCreate): Data for new task creation

        Returns:
            TaskResponse: Newly created task
        """
        task = self.task_repository.create_task(task)
        response_task = TaskResponse.model_validate(task)
        self.task_cache.add_task(response_task)
        return response_task

    def update_task(self, task_update: TaskUpdate) -> TaskResponse:
        """Update an existing task.

        Args:
            task_update (TaskUpdate): Task update data

        Returns:
            TaskResponse: Updated task

        Raises:
            FileNotFoundError: If task with given ID doesn't exist
        """
        task = self.task_repository.get_task_by_id(task_update.task_id)
        if not task:
            raise FileNotFoundError(f"Task {task_update.task_id} not found")

        updated_task = self.task_repository.update_task(task_update)
        self.task_cache.invalidate_cache()
        return TaskResponse.model_validate(updated_task)

    def delete_task(self, task_id: UUID) -> None:

        self.task_repository.delete_task(task_id)
        self.task_cache.invalidate_cache()
