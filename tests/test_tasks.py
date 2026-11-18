from backend.task_schemas import TaskCreate, TaskUpdate


def test_task_create_schema():
    task = TaskCreate(
        title="Receive Customer Query",
        description="Receive customer support query",
        priority="high",
        workflow_id=1
    )

    assert task.title == "Receive Customer Query"
    assert task.priority == "high"
    assert task.workflow_id == 1


def test_task_update_schema():
    task = TaskUpdate(
        title="Updated Customer Query",
        status="in_progress"
    )

    assert task.title == "Updated Customer Query"
    assert task.status == "in_progress"


def test_task_create_schema_invalid_title():
    from pydantic import ValidationError
    import pytest

    with pytest.raises(ValidationError):
        TaskCreate(
            title="A",
            description="Invalid task",
            priority="high",
            workflow_id=1
        )