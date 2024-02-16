from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    text: str
    day: str
    reminder: bool


class Task(TaskBase):
    id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    text: Optional[str] = None
    day: Optional[str] = None
    reminder: Optional[bool] = None
