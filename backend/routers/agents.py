
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User
from backend.agent_models import Agent
from backend.agent_schemas import AgentCreate, AgentResponse, AgentUpdate
from backend.security import get_current_user

router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)


# CREATE AGENT
@router.post("/", response_model=AgentResponse)
def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_agent = Agent(
        name=agent_data.name,
        description=agent_data.description,
        agent_type=agent_data.agent_type,
        owner_id=current_user.id
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return new_agent


# GET ALL AGENTS
@router.get("/", response_model=list[AgentResponse])
def get_agents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    agents = db.query(Agent).filter(
        Agent.owner_id == current_user.id
    ).all()

    return agents


# UPDATE AGENT
@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    update_data = agent_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(agent, key, value)

    db.commit()
    db.refresh(agent)

    return agent


# DELETE AGENT
@router.delete("/{agent_id}")
def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    db.delete(agent)
    db.commit()

    return {
        "message": "Agent deleted successfully"
    }
