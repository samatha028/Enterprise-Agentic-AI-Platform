from backend.workflow_schemas import WorkflowCreate, WorkflowUpdate


def test_workflow_create_schema():
    workflow = WorkflowCreate(
        name="Customer Support Workflow",
        description="Automates customer support"
    )

    assert workflow.name == "Customer Support Workflow"
    assert workflow.description == "Automates customer support"


def test_workflow_update_schema():
    workflow = WorkflowUpdate(
        name="Updated Customer Support Workflow"
    )

    assert workflow.name == "Updated Customer Support Workflow"


def test_workflow_create_schema_invalid_name():
    from pydantic import ValidationError
    import pytest

    with pytest.raises(ValidationError):
        WorkflowCreate(
            name="A",
            description="Invalid workflow"
        )