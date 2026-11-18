from backend.execution_schemas import ExecutionCreate, ExecutionResponse


def test_execution_create_schema():
    execution = ExecutionCreate(
        task_id=1
    )

    assert execution.task_id == 1


def test_execution_response_schema():
    execution = ExecutionResponse(
        id=1,
        task_id=1,
        owner_id=2,
        status="running",
        result=None,
        error_message=None
    )

    assert execution.id == 1
    assert execution.task_id == 1
    assert execution.status == "running"
    assert execution.result is None


def test_execution_response_completed():
    execution = ExecutionResponse(
        id=1,
        task_id=1,
        owner_id=2,
        status="completed",
        result="Task executed successfully",
        error_message=None
    )

    assert execution.status == "completed"
    assert execution.result == "Task executed successfully"


def test_execution_response_failed():
    execution = ExecutionResponse(
        id=2,
        task_id=1,
        owner_id=2,
        status="failed",
        result=None,
        error_message="Execution failed"
    )

    assert execution.status == "failed"
    assert execution.error_message == "Execution failed"