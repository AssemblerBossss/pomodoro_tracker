import json

from redis import Redis
from schema import TaskResponse


class TaskCache:

    def __init__(self, redis: Redis):
        self.redis = redis
        self.cache_key = "tasks_list"

    def get_tasks(self) -> list[TaskResponse]:
        with self.redis as redis:
            # Получаем все элементы списка
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
        if not tasks:  # Проверка на пустой список
            self.invalidate_cache()
            return

        tasks_json = [task.model_dump_json() for task in tasks]
        with self.redis as redis:
            redis.delete(self.cache_key)
            redis.rpush(self.cache_key, *tasks_json)
            redis.expire(self.cache_key, 300)

    def add_task(self, task: TaskResponse) -> None:
        """Добавление одной задачи в кэш"""
        with self.redis as redis:
            redis.rpush(self.cache_key, task.model_dump_json())

    def invalidate_cache(self) -> None:
        """Очистка кэша"""
        with self.redis as redis:
            redis.delete(self.cache_key)
