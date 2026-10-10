from agent.agent import TaskPilotAgent
from agent.state import AgentState


def test_agent_initial_state():
    agent=TaskPilotAgent()

    assert agent.state==AgentState.IDLE
    assert agent.state_history==[]


def test_create_plan_updates_state():
    agent=TaskPilotAgent()

    agent.understand("Process invoice INV-1042")
    plan=agent.create_plan()

    assert len(plan)==4
    assert agent.state==AgentState.READY
    assert agent.state_history==[
        {"from":"idle","to":"planning"},
        {"from":"planning","to":"ready"}
    ]


def test_agent_rejects_empty_task():
    agent=TaskPilotAgent()

    try:
        agent.understand("")
        assert False,"Expected ValueError for an empty task"
    except ValueError as exc:
        assert "non-empty string" in str(exc)


def test_agent_rejects_task_after_planning():
    agent=TaskPilotAgent()

    agent.understand("Process invoice INV-1042")
    agent.create_plan()

    try:
        agent.understand("Process invoice INV-9999")
        assert False,"Expected ValueError after planning"
    except ValueError as exc:
        assert "already started" in str(exc)


def test_agent_fails_when_invoice_number_missing():
    agent=TaskPilotAgent()
    agent.understand("Process the next available invoice")

    result=agent.execute()

    assert result["status"]=="failed"
    assert "invoice number" in result["error"].lower()
    assert agent.state==AgentState.FAILED


def test_failed_agent_does_not_execute_again():
    agent=TaskPilotAgent()
    agent.understand("Process the next available invoice")

    first_result=agent.execute()
    second_result=agent.execute()

    assert first_result is second_result
    assert agent.state==AgentState.FAILED