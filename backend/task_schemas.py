from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: Optional[str] = None
    priority: str = "medium"
    workflow_id: int


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    workflow_id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None