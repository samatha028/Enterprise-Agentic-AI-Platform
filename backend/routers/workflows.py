from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User
from backend.workflow_models import Workflow
from backend.workflow_schemas import (
    WorkflowCreate,
    WorkflowResponse,
    WorkflowUpdate
)
from backend.security import get_current_user

router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)


# CREATE WORKFLOW
@router.post("/", response_model=WorkflowResponse)
def create_workflow(
    workflow_data: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_workflow = Workflow(
        name=workflow_data.name,
        description=workflow_data.description,
        owner_id=current_user.id
    )

    db.add(new_workflow)
    db.commit()
    db.refresh(new_workflow)

    return new_workflow


# GET ALL WORKFLOWS
@router.get("/", response_model=list[WorkflowResponse])
def get_workflows(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflows = db.query(Workflow).filter(
        Workflow.owner_id == current_user.id
    ).all()

    return workflows


# UPDATE WORKFLOW
@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(
    workflow_id: int,
    workflow_data: WorkflowUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.owner_id == current_user.id
    ).first()

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    update_data = workflow_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(workflow, key, value)

    db.commit()
    db.refresh(workflow)

    return workflow


# DELETE WORKFLOW
@router.delete("/{workflow_id}")
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.owner_id == current_user.id
    ).first()

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    db.delete(workflow)
    db.commit()

    return {
        "message": "Workflow deleted successfully"
    }