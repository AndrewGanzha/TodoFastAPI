from typing import List

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    todo: str = Field(min_length=1, max_length=320)


class TodoGet(TodoBase):
    id: int
    user_id: int

    model_config = {"from_attributes": True}


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    id: int


class TodoDelete(BaseModel):
    id: int


class TodoList(BaseModel):
    todos: List[TodoGet]
