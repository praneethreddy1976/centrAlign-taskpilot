
from enum import Enum


class AgentState(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    READY = "ready"
    RUNNING = "running"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


ALLOWED_TRANSITIONS = {
    AgentState.IDLE: {AgentState.PLANNING, AgentState.FAILED},
    AgentState.PLANNING: {AgentState.READY, AgentState.FAILED},
    AgentState.READY: {AgentState.RUNNING, AgentState.FAILED},
    AgentState.RUNNING: {
        AgentState.VERIFYING,
        AgentState.FAILED
    },
    AgentState.VERIFYING: {
        AgentState.COMPLETED,
        AgentState.FAILED
    },
    AgentState.COMPLETED: set(),
    AgentState.FAILED: set()
}


def can_transition(current_state, next_state):
    return next_state in ALLOWED_TRANSITIONS[current_state]


def transition(current_state, next_state):
    if not can_transition(current_state, next_state):
        raise ValueError(
            f"Invalid state transition: "
            f"{current_state.value} -> {next_state.value}"
        )

    return next_state
