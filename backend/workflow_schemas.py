from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class WorkflowCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None


class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    description: Optional[str] = None
    status: Optional[str] = None