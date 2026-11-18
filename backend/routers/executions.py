from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from backend.database import get_db
from backend.execution_models import Execution
from backend.execution_schemas import (
    ExecutionCreate,
    ExecutionResponse
)
from backend.task_models import Task
from backend.security import get_current_user
from backend.models import User


router = APIRouter(
    prefix="/executions",
    tags=["Executions"]
)


@router.post("/", response_model=ExecutionResponse)
def create_execution(
    execution_data: ExecutionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == execution_data.task_id,
        Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    new_execution = Execution(
        task_id=task.id,
        owner_id=current_user.id,
        status="running",
        started_at=datetime.now(timezone.utc)
    )

    db.add(new_execution)
    db.commit()
    db.refresh(new_execution)

    return new_execution


@router.get("/", response_model=list[ExecutionResponse])
def get_executions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    executions = db.query(Execution).filter(
        Execution.owner_id == current_user.id
    ).all()

    return executions


@router.get("/{execution_id}", response_model=ExecutionResponse)
def get_execution(
    execution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    execution = db.query(Execution).filter(
        Execution.id == execution_id,
        Execution.owner_id == current_user.id
    ).first()

    if not execution:
        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    return execution


@router.put("/{execution_id}/complete")
def complete_execution(
    execution_id: int,
    result: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    execution = db.query(Execution).filter(
        Execution.id == execution_id,
        Execution.owner_id == current_user.id
    ).first()

    if not execution:
        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    execution.status = "completed"
    execution.result = result
    execution.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(execution)

    return {
        "message": "Execution completed successfully",
        "execution_id": execution.id,
        "status": execution.status,
        "result": execution.result
    }


@router.put("/{execution_id}/fail")
def fail_execution(
    execution_id: int,
    error_message: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    execution = db.query(Execution).filter(
        Execution.id == execution_id,
        Execution.owner_id == current_user.id
    ).first()

    if not execution:
        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    execution.status = "failed"
    execution.error_message = error_message
    execution.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(execution)

    return {
        "message": "Execution marked as failed",
        "execution_id": execution.id,
        "status": execution.status,
        "error_message": execution.error_message
    }