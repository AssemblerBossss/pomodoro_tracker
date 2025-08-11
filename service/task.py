from repository import TaskRepository, TaskCache
from schema import TaskResponse, TaskCreate
from dataclasses import dataclass


@dataclass
class TaskService:

    task_repository : TaskRepository
    task_cache : TaskCache

    def get_tasks(self) ->list[TaskResponse] :
        """
        Получить все задачи.

        :return:
            list[TaskResponse]: Список задач из кэша (если есть) или БД
        """
        if cached := self.task_cache.get_tasks():
            return cached

        tasks = [TaskResponse.model_validate(t) for t in self.task_repository.get_all_tasks()]
        self.task_cache.set_tasks(tasks)
        return tasks

    def create_task(self, task: TaskCreate) -> TaskResponse:
        """
        Создать новую задачу.

        :param task: (TaskCreate): Данные для создания задачи
        :return TaskResponse: Созданная задача (добавляется в кэш)
        """
        task = self.task_repository.create_task(task)
        response_task = TaskResponse.model_validate(task)
        self.task_cache.add_task(TaskResponse.model_validate(response_task))
        return response_task
