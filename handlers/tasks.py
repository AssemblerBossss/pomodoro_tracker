from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, status, Depends
from schema import TaskCreate, TaskResponse, TaskUpdate
from dependency import get_task_service, get_request_user_id
from service import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[TaskResponse])
async def get_tasks(task_service: Annotated[TaskService, Depends(get_task_service)]):
    return task_service.get_tasks()


@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: UUID = Depends(get_request_user_id)
):
    return task_service.create_task(task, user_id)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task: TaskUpdate, task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.update_task(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID, task_service: Annotated[TaskService, Depends(get_task_service)]
):
    task_service.delete_task(task_id)


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
