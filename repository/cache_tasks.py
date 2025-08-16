import json

from redis import Redis
from schema import TaskResponse


class TaskCache:
    """Redis-based cache for storing and retrieving task data.

    Provides methods for caching task lists and individual tasks with JSON serialization.

    Attributes:
        redis: Redis client instance
        cache_key: Key used for storing tasks in Redis (default: "tasks_list")
    """

    def __init__(self, redis: Redis):
        """Initialize TaskCache with Redis connection.

        Args:
            redis: Configured Redis client instance
        """
        self.redis = redis
        self.cache_key = "tasks_list"

    def get_tasks(self) -> list[TaskResponse]:
        """Retrieve all tasks from cache.

        Returns:
            List of TaskResponse objects if cache exists, empty list otherwise
        """
        with self.redis as redis:
            tasks_data = redis.lrange(self.cache_key, 0, -1)
            # Декодируем каждый элемент и парсим JSON
            return (
                [
                    TaskResponse.model_validate(json.loads(task.decode("utf-8")))
                    for task in tasks_data
                ]
                if tasks_data
                else []
            )

    def set_tasks(self, tasks: list[TaskResponse]) -> None:
        """Cache a list of tasks with 5 minute expiration.

        Args:
            tasks: List of TaskResponse objects to cache

        Note:
            If empty list is provided, cache will be invalidated
        """
        if not tasks:
            self.invalidate_cache()
            return

        tasks_json = [task.model_dump_json() for task in tasks]
        with self.redis as redis:
            redis.delete(self.cache_key)
            redis.rpush(self.cache_key, *tasks_json)
            redis.expire(self.cache_key, 300)

    def add_task(self, task: TaskResponse) -> None:
        """Append single task to existing cache.

        Args:
            task: TaskResponse object to add to cache
        """
        with self.redis as redis:
            redis.rpush(self.cache_key, task.model_dump_json())

    def invalidate_cache(self) -> None:
        """Clear all cached task data."""
        with self.redis as redis:
            redis.delete(self.cache_key)
