import json

from redis import Redis
from schema import TaskResponse


class TaskCache:

    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[TaskResponse]:
        with self.redis as redis:
            # Получаем все элементы списка
            tasks_data = redis.lrange('tasks', 0, -1)
            # Декодируем каждый элемент и парсим JSON
            return [
                TaskResponse.model_validate(json.loads(task.decode('utf-8')))
                for task in tasks_data
            ]

    def set_tasks(self, tasks: list[TaskResponse]) -> None:
        tasks_json = [task.model_dump_json() for task in tasks]
        with self.redis as redis:
            # Удаляем старый список (опционально)
            redis.delete('tasks')
            # Добавляем новые задачи
            redis.lpush("tasks", *tasks_json)
