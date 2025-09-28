from typing import List
from uuid import UUID
from repository import TaskRepository, TaskCache
from schema import TaskResponse, TaskCreate, TaskUpdate
from dataclasses import dataclass

from exception import TaskNotFoundException


@dataclass
class TaskService:
    """Service layer for task operations with Redis caching.

    Coordinates between task repository (database) and task cache (Redis).
    """

    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_user_tasks(self, user_id: UUID) -> List[TaskResponse]:
        """Extract all user's tasks from the cache or database.

        Returns cached tasks if available, otherwise fetches from database,
        updates cache, and returns the results.

        Args:
            user_id (UUID): User ID

        Returns:
            List[TaskResponse]: List of all tasks
        """
        if cached := await self.task_cache.get_user_tasks(user_id):
            return cached

        tasks = [
            TaskResponse.model_validate(t)
            for t in await self.task_repository.get_user_tasks(user_id)
        ]
        await self.task_cache.set_users_task(user_id=user_id, tasks=tasks)
        return tasks

    async def create_task(self, task: TaskCreate, user_id: UUID) -> TaskResponse:
        """Create a new task and add it to cache.

        Args:
            task (TaskCreate): Data for new task creation
            user_id (UUID): User ID

        Returns:
            TaskResponse: Newly created task
        """
        task_id: UUID = await self.task_repository.create_task(task, user_id)
        task = await self.task_repository.get_task_by_id(task_id)
        response_task = TaskResponse.model_validate(task)
        await self.task_cache.add_task(user_id=user_id, task=response_task)
        return response_task

    async def update_task(self, task_update: TaskUpdate, user_id: UUID) -> TaskResponse:
        """Update an existing task.

        Args:
            task_update (TaskUpdate): Task update data
            user_id (UUID): User ID

        Returns:
            TaskResponse: Updated task

        Raises:
            TaskNotFoundException: If task with given ID doesn't exist
        """
        task = await self.task_repository.get_user_task(
            task_id=task_update.task_id, user_id=user_id
        )
        if not task:
            raise TaskNotFoundException

        updated_task = await self.task_repository.update_task(task_update)
        await self.task_cache.invalidate_user_cache(user_id=user_id)
        return TaskResponse.model_validate(updated_task)

    async def delete_task(self, task_id: UUID, user_id: UUID) -> None:
        """Delete task.

        Args:
            task_id (UUID): Task ID
            user_id (UUID): User ID
        """
        task = await self.task_repository.get_user_task(
            task_id=task_id, user_id=user_id
        )
        if not task:
            raise TaskNotFoundException
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)
        await self.task_cache.invalidate_user_cache(user_id=user_id)
