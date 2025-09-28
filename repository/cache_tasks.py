import json
from uuid import UUID
from redis import asyncio as aioredis

from schema import TaskResponse


class TaskCache:
    """Redis-based cache for storing and retrieving task data.

    Provides methods for caching task lists and individual tasks with JSON serialization.

    Attributes:
        aioredis: Redis client instance
    """

    def __init__(self, _aioredis: aioredis.Redis):
        """Initialize TaskCache with Redis connection.

        Args:
            _aioredis: Configured Redis client instance
        """
        self.aioredis = _aioredis

    async def get_user_tasks(self, user_id: UUID) -> list[TaskResponse]:
        """Retrieve all user's tasks from cache.

        Args:
            user_id: User ID

        Returns:
            List of TaskResponse objects if cache exists, empty list otherwise
        """
        cache_key = f"user_tasks:{user_id}"

        async with self.aioredis as redis:
            tasks_data = await redis.lrange(cache_key, 0, -1)
            return (
                [
                    TaskResponse.model_validate(json.loads(task.decode("utf-8")))
                    for task in tasks_data
                ]
                if tasks_data
                else []
            )

    async def set_users_task(self, user_id: UUID, tasks: list[TaskResponse]) -> None:
        """Cache a list of tasks with 5 minute expiration.

        Args:
            tasks: List of TaskResponse objects to cache
            user_id: User ID

        Note:
            If empty list is provided, cache will be invalidated
        """
        cache_key = f"user_tasks:{str(user_id)}"

        if not tasks:
            await self.invalidate_user_cache(user_id=user_id)
            return

        tasks_json = [task.model_dump_json() for task in tasks]
        async with self.aioredis as redis:
            await redis.delete(cache_key)
            await redis.rpush(cache_key, *tasks_json)
            await redis.expire(cache_key, 300)

    async def add_task(self, user_id: UUID, task: TaskResponse) -> None:
        """Append single task to existing cache.

        Args:
            task: TaskResponse object to add to cache
            user_id: User ID
        """
        cache_key = f"user_tasks:{str(user_id)}"

        async with self.aioredis as redis:
            await redis.rpush(cache_key, task.model_dump_json())

    async def invalidate_user_cache(self, user_id: UUID) -> None:
        """Clear all cached task data."""
        async with self.aioredis as redis:
            await redis.delete(str(user_id))
