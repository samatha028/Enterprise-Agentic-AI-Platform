from pydantic import BaseModel, ConfigDict
from typing import Optional


class ExecutionCreate(BaseModel):
    task_id: int


class ExecutionResponse(BaseModel):
    id: int
    task_id: int
    owner_id: int
    status: str
    result: Optional[str] = None
    error_message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)