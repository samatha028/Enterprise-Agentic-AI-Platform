from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User
from backend.workflow_models import Workflow
from backend.task_models import Task
from backend.task_schemas import (
    TaskCreate,
    TaskResponse,
    TaskUpdate
)
from backend.security import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# CREATE TASK
@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflow = db.query(Workflow).filter(
        Workflow.id == task_data.workflow_id,
        Workflow.owner_id == current_user.id
    ).first()

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        workflow_id=task_data.workflow_id,
        owner_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# GET ALL TASKS
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = db.query(Task).filter(
        Task.owner_id == current_user.id
    ).all()

    return tasks


# UPDATE TASK
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# DELETE TASK
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }