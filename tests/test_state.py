import pytest

from agent.state import AgentState, can_transition, transition


def test_valid_transition():
    result=transition(AgentState.IDLE,AgentState.PLANNING)

    assert result==AgentState.PLANNING


def test_invalid_transition():
    with pytest.raises(ValueError):
        transition(AgentState.IDLE,AgentState.COMPLETED)


def test_idle_can_enter_failed():
    assert can_transition(
        AgentState.IDLE,
        AgentState.FAILED
    )


def test_running_can_enter_verifying():
    assert can_transition(
        AgentState.RUNNING,
        AgentState.VERIFYING
    )


def test_completed_is_terminal():
    assert not can_transition(
        AgentState.COMPLETED,
        AgentState.FAILED
    )

    assert not can_transition(
        AgentState.COMPLETED,
        AgentState.RUNNING
    )


def test_failed_is_terminal():
    assert not can_transition(
        AgentState.FAILED,
        AgentState.RUNNING
    )

    assert not can_transition(
        AgentState.FAILED,
        AgentState.COMPLETED
    )