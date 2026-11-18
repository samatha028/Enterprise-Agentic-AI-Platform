from backend.agent_schemas import AgentCreate, AgentUpdate


def test_agent_create_schema():
    agent = AgentCreate(
        name="Customer Support Agent",
        description="Handles customer queries",
        agent_type="Customer Support"
    )

    assert agent.name == "Customer Support Agent"
    assert agent.agent_type == "Customer Support"


def test_agent_update_schema():
    agent = AgentUpdate(
        name="Updated Support Agent"
    )

    assert agent.name == "Updated Support Agent"
def test_agent_create_schema_invalid_name():
    from pydantic import ValidationError
    import pytest

    with pytest.raises(ValidationError):
        AgentCreate(
            name="A",
            description="Invalid agent",
            agent_type="Support"
        )