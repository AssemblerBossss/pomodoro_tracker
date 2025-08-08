from uuid import UUID
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    category_id: UUID

    class Config:
        from_attributes = True
