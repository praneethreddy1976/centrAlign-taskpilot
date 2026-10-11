from agent.agent import TaskPilotAgent
import agent.agent as agent_module
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

def test_agent_has_unique_execution_ids():
    first=TaskPilotAgent()
    second=TaskPilotAgent()

    assert first.execution_id
    assert second.execution_id
    assert first.execution_id!=second.execution_id



def test_successful_execution_records_audit_history(monkeypatch):
    invoice={
        "company":"Test Company",
        "invoice":"INV-1042",
        "date":"2026-10-01",
        "amount":1000,
        "due_date":"2026-10-31"
    }

    monkeypatch.setattr(
        agent_module,
        "get_invoices",
        lambda:[invoice]
    )
    monkeypatch.setattr(
        agent_module,
        "save_invoice",
        lambda invoice:"Invoice saved successfully"
    )
    monkeypatch.setattr(
        agent_module,
        "verify_invoice",
        lambda invoice:True
    )

    agent=TaskPilotAgent()
    agent.understand("Process invoice INV-1042")

    result=agent.execute()

    assert result["status"]=="completed"
    assert agent.execution_history[0]["event"]=="state_transition"
    assert any(
        event["event"]=="execution_started"
        for event in agent.execution_history
    )
    assert any(
        event["event"]=="execution_finished"
        and event["status"]=="completed"
        for event in agent.execution_history
    )



def test_failed_execution_records_failure_reason(monkeypatch):
    monkeypatch.setattr(
        agent_module,
        "get_invoices",
        lambda:[]
    )

    agent=TaskPilotAgent()
    agent.understand("Process invoice INV-9999")

    result=agent.execute()

    assert result["status"]=="failed"
    assert any(
        event["event"]=="execution_finished"
        and event["status"]=="failed"
        and event["failure_reason"]==result["error"]
        for event in agent.execution_history
    )



def test_repeated_execution_does_not_duplicate_audit_events(monkeypatch):
    invoice={
        "company":"Test Company",
        "invoice":"INV-1042",
        "date":"2026-10-01",
        "amount":1000,
        "due_date":"2026-10-31"
    }

    monkeypatch.setattr(
        agent_module,
        "get_invoices",
        lambda:[invoice]
    )
    monkeypatch.setattr(
        agent_module,
        "save_invoice",
        lambda invoice:"Invoice saved successfully"
    )
    monkeypatch.setattr(
        agent_module,
        "verify_invoice",
        lambda invoice:True
    )

    agent=TaskPilotAgent()
    agent.understand("Process invoice INV-1042")

    first_result=agent.execute()
    history_before=agent.execution_history.copy()

    second_result=agent.execute()

    assert first_result["status"]=="completed"
    assert second_result is first_result
    assert agent.execution_history==history_before

def test_existing_matching_invoice_is_reconciled(monkeypatch):
    invoice={
        "company":"Acme Corp",
        "invoice":"INV-1042",
        "date":"2026-10-05",
        "amount":48500,
        "due_date":"2026-10-20"
    }

    monkeypatch.setattr(
        agent_module,
        "get_invoices",
        lambda:[invoice]
    )
    monkeypatch.setattr(
        agent_module,
        "save_invoice",
        lambda invoice:"Invoice already exists"
    )
    monkeypatch.setattr(
        agent_module,
        "verify_invoice",
        lambda invoice:True
    )

    agent=TaskPilotAgent()
    agent.understand("Process invoice INV-1042")

    result=agent.execute()

    assert result["status"]=="completed"
    assert result["verified"] is True
    assert result["finance_message"]=="Invoice already existed and was verified"
    assert "Enter invoice details into the finance system" not in result["completed_steps"]
    assert any(
        event["event"]=="duplicate_invoice_detected"
        for event in agent.execution_history
    )

def test_existing_mismatched_invoice_requires_review(monkeypatch):
    invoice={
        "company":"Acme Corp",
        "invoice":"INV-1042",
        "date":"2026-10-05",
        "amount":48500,
        "due_date":"2026-10-20"
    }

    monkeypatch.setattr(
        agent_module,
        "get_invoices",
        lambda:[invoice]
    )
    monkeypatch.setattr(
        agent_module,
        "save_invoice",
        lambda invoice:"Invoice already exists"
    )
    monkeypatch.setattr(
        agent_module,
        "verify_invoice",
        lambda invoice:False
    )

    agent=TaskPilotAgent()
    agent.understand("Process invoice INV-1042")

    result=agent.execute()

    assert result["status"]=="failed"
    assert "human review required" in result["error"].lower()
    assert result["save_outcome"]=="already_exists"
    assert result["verification_status"]=="failed"
    assert any(
        event["event"]=="duplicate_invoice_mismatch"
        for event in agent.execution_history
    )
