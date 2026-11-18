from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class AgentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    agent_type: str = Field(min_length=2, max_length=50)


class AgentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    agent_type: str
    status: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
class AgentUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    description: Optional[str] = None
    agent_type: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    status: Optional[str] = None