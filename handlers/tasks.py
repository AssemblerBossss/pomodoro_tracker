from typing import Annotated
from fastapi import APIRouter, status, Depends
from repository import TaskRepository
from schema import TaskCreate, TaskResponse
from dependency import get_tasks_repository
from schema.task import TaskUpdate

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[TaskResponse])
async def get_tasks(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
):
    tasks = task_repository.get_all_tasks()
    return tasks


@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
):
    response_task = task_repository.create_task(task)
    return response_task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task: TaskUpdate,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
):
    return task_repository.update_task(task)


#
# # @router.put(
# #     "/{task_id}",
# #     response_model=TaskSchema)
# # async def update_task(task_id: int, name: str):
# #     for task in fixture_tasks:
# #         if task["id"] == task_id:
# #             task["name"] = name
# #             return task
#
#


# @router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_task(task_id: int):
#     for index, task in enumerate(fixture_tasks):
#         if task["id"] == task_id:
#             fixture_tasks.pop(index)
#             return
#     return {"message": "Task not found"}
#
