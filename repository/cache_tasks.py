from redis import Redis
from schema import TaskResponse


class TaskCache:

    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self):
        pass

    def set_tasks(self, tasks: list[TaskResponse]):
        tasks_json = [task.model_dump_json() for task in tasks]
        self.redis.lpush("tasks", *tasks_json)
