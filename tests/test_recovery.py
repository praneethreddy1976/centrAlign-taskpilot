from agent.agent import TaskPilotAgent
from agent.state import AgentState


def test_lookup_recovers_after_transient_error(monkeypatch):
    agent=TaskPilotAgent()
    calls={"count":0}

    def mock_find_invoice(invoice_number):
        calls["count"]+=1

        if calls["count"]==1:
            raise ConnectionError("Temporary connection failure")

        return {
            "invoice":invoice_number,
            "company":"Acme Corp",
            "amount":48500,
            "due_date":"2026-10-20"
        }

    monkeypatch.setattr(agent,"find_invoice",mock_find_invoice)

    invoice=agent._find_invoice_with_retry("INV-1042")

    assert invoice["invoice"]=="INV-1042"
    assert calls["count"]==2
    assert agent.lookup_attempts==2
    assert len(agent.recovery_history)==2
    assert agent.recovery_history[0]["status"]=="error"
    assert agent.recovery_history[1]["status"]=="found"


def test_lookup_stops_after_two_errors(monkeypatch):
    agent=TaskPilotAgent()
    calls={"count":0}

    def mock_find_invoice(invoice_number):
        calls["count"]+=1
        raise ConnectionError("Temporary connection failure")

    monkeypatch.setattr(agent,"find_invoice",mock_find_invoice)

    try:
        agent._find_invoice_with_retry("INV-1042")
        assert False,"Expected the lookup to fail"
    except ConnectionError:
        pass

    assert calls["count"]==2
    assert agent.lookup_attempts==2
    assert len(agent.recovery_history)==2


def test_missing_invoice_is_not_retried(monkeypatch):
    agent=TaskPilotAgent()
    calls={"count":0}

    def mock_find_invoice(invoice_number):
        calls["count"]+=1
        return None

    monkeypatch.setattr(agent,"find_invoice",mock_find_invoice)

    invoice=agent._find_invoice_with_retry("INV-9999")

    assert invoice is None
    assert calls["count"]==1
    assert agent.lookup_attempts==1
    assert agent.recovery_history[0]["status"]=="not_found"


def test_execute_fails_after_lookup_errors(monkeypatch):
    agent=TaskPilotAgent()
    agent.understand("Process invoice INV-1042")

    def mock_find_invoice(invoice_number):
        raise ConnectionError("Portal unavailable")

    monkeypatch.setattr(agent,"find_invoice",mock_find_invoice)

    result=agent.execute()

    assert result["status"]=="failed"
    assert agent.state==AgentState.FAILED
    assert agent.lookup_attempts==2
    assert len(agent.recovery_history)==2