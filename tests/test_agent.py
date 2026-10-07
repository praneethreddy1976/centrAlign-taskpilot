from agent.agent import TaskPilotAgent


def test_agent_understands_task():
    agent=TaskPilotAgent()

    result=agent.understand("Process invoice INV-1042")

    assert result["status"]=="understood"
    assert result["goal"]=="Process invoice INV-1042"


def test_agent_creates_plan():
    agent=TaskPilotAgent()

    agent.understand("Process invoice INV-1042")
    plan=agent.create_plan()

    assert len(plan)==4
    assert plan[0]=="Find the requested invoice"
    assert plan[-1]=="Verify the saved invoice"


def test_agent_finds_invoice():
    agent=TaskPilotAgent()

    agent.understand("Process invoice INV-1042")

    invoice=agent.find_invoice("INV-1042")

    assert invoice is not None
    assert invoice["invoice"]=="INV-1042"
    assert invoice["company"]=="Acme Corp"
    assert invoice["amount"]==48500
    assert invoice["due_date"]=="2026-10-20"


def test_agent_invoice_not_found():
    agent=TaskPilotAgent()

    agent.understand("Process invoice INV-9999")

    invoice=agent.find_invoice("INV-9999")

    assert invoice is None


def test_agent_plan_has_verification_step():
    agent=TaskPilotAgent()

    agent.understand("Process invoice INV-1042")
    plan=agent.create_plan()

    assert "Verify the saved invoice" in plan    