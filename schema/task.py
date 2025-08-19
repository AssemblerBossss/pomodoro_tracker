from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    pomodoro_count: int = Field(ge=0)
    category_id: Optional[UUID] = Field(
        None, description="ID категории (опционально)"  # Значение по умолчанию
    )


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    task_id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class TaskUpdate(TaskBase):
    task_id: UUID
