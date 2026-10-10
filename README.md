# CentrAlign TaskPilot

An autonomous AI task worker prototype inspired by the CentrAlign AI Engineering Hiring Challenge.

## About the Project

CentrAlign TaskPilot is a prototype of an autonomous AI task worker designed to understand a user's goal, create a plan, interact with computer-based tools, execute tasks, observe results, recover from certain failures, verify outcomes, and report completion.

The current implementation focuses on invoice processing in a controlled local company environment.

The demonstration task is:

`Process invoice INV-1042`

The agent retrieves invoice details from a local Invoice Portal, submits the information to a local Finance System, and independently verifies that the invoice was saved.

The project is intentionally being developed as a working prototype before expanding toward more general-purpose autonomous task execution.

## Current Capabilities

- Natural-language task input
- Task understanding and execution planning
- Browser automation using Playwright
- Structured invoice extraction
- Finance-system interaction
- Independent invoice verification
- Explicit agent lifecycle states
- State-transition validation
- Task input validation
- Execution failure handling
- Bounded retry logic for invoice lookup
- Recovery-attempt logging
- Protection against repeating a completed or failed execution
- Automated tests using Pytest

## Architecture

The current execution workflow is:

User Goal
  ↓
TaskPilot Agent
  ↓
Understand Task
  ↓
Create Plan
  ↓
Find Invoice
  ↓
Extract Invoice Details
  ↓
Finance Tool
  ↓
Save Invoice
  ↓
Independent Verification
  ↓
Report Result

The main engineering principle is to separate agent orchestration from deterministic computer-interaction tools.

The agent coordinates the workflow and manages execution state. The tools interact with the local applications, while the verification layer checks whether the expected outcome actually exists.

## Local Environment

The prototype contains two Flask web applications.

### 1. Invoice Portal

URL: `http://127.0.0.1:8000`

The Invoice Portal contains sample invoices from:

- Acme Corp
- Beta Industries
- Gamma Solutions

The demonstration invoice is:

- Company: Acme Corp
- Invoice Number: INV-1042
- Invoice Date: 2026-10-05
- Amount: 48500
- Due Date: 2026-10-20

### 2. Finance System

URL: `http://127.0.0.1:8001`

The Finance System provides a form for entering invoice information.

The form contains:

- Company
- Invoice Number
- Amount
- Due Date
- Save Invoice

After submission, the saved invoice can be checked in the application's Saved Invoices table.

## Browser Automation

Browser automation is implemented using Playwright and Chromium.

The browser tool can:

1. Open the Invoice Portal.
2. Read invoice information from the webpage.
3. Convert the observed information into structured Python data.
4. Return the invoice information to the agent.

The finance tool can:

1. Open the Finance System.
2. Fill the invoice form.
3. Submit the invoice.
4. Observe the application's response.

The agent uses these tools instead of directly implementing browser interactions inside its orchestration logic.

## Agent Implementation

The main agent is implemented in:

`src/agent/agent.py`

The state machine is implemented in:

`src/agent/state.py`

The agent currently supports the following operations.

### Understand

The agent receives a task such as:

`Process invoice INV-1042`

It validates the input and stores the task as its current goal.

### Plan

The agent creates a four-step plan:

1. Find the requested invoice.
2. Extract invoice details.
3. Enter invoice details into the finance system.
4. Verify the saved invoice.

### Find Invoice

The agent calls the browser tool to retrieve invoice data and searches for the requested invoice number.

### Execute

The agent coordinates invoice retrieval, finance-system submission, and verification.

It records completed steps and returns a structured result indicating success or failure.

### Verify

The agent calls the independent verification layer after submission.

A success message from the Finance System alone is not considered sufficient evidence of successful completion.

## Agent State Management

The agent uses an explicit state machine to track execution.

The available states are:

- `IDLE` — The agent has not started planning.
- `PLANNING` — The execution plan is being created.
- `READY` — The plan is ready to execute.
- `RUNNING` — Invoice retrieval and submission are in progress.
- `VERIFYING` — The saved invoice is being checked.
- `COMPLETED` — The requested workflow succeeded.
- `FAILED` — The workflow failed.

The normal successful transition sequence is:

`IDLE → PLANNING → READY → RUNNING → VERIFYING → COMPLETED`

Invalid transitions are rejected by the state machine.

The agent also records its state history, allowing the execution lifecycle to be inspected after a run.

## Failure Handling and Recovery

The agent validates task input and handles failures during execution.

Current failure-handling capabilities include:

- Rejecting empty task descriptions
- Detecting when an invoice number cannot be extracted
- Handling missing invoices
- Capturing unexpected execution exceptions
- Recording failure information
- Preventing repeated execution after completion or failure

### Bounded Invoice Lookup Recovery

The agent can retry invoice lookup up to two times when the lookup raises an exception.

Each lookup attempt is recorded in `recovery_history`, including the attempt number and outcome.

If an invoice is not found, the agent does not repeatedly search for the same missing invoice through the retry mechanism.

Automatic retries are limited to invoice lookup. The invoice-saving operation is not automatically retried because repeating a side-effecting operation could create duplicate records.

Recovery is currently limited to this specific lookup operation; it is not yet a general-purpose recovery system.

## Independent Verification

The verification layer is implemented in:

`src/verification/verifier.py`

It checks whether the expected invoice exists in the Finance System's Saved Invoices table.

The verification checks include:

- Company
- Invoice Number
- Amount
- Due Date

The verifier independently inspects the saved data rather than relying only on the success message returned by the finance tool.

## Project Structure

```text
centrAlign-taskpilot/
├── src/
│   ├── agent/
│   │   ├── agent.py
│   │   └── state.py
│   ├── environment/
│   │   ├── invoice_portal.py
│   │   └── finance_app.py
│   ├── tools/
│   │   ├── browser.py
│   │   └── finance_tool.py
│   ├── verification/
│   │   └── verifier.py
│   └── main.py
├── tests/
│   ├── test_agent.py
│   ├── test_agent_state.py
│   ├── test_recovery.py
│   └── test_state.py
├── data/
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

The `.venv` and `.git` directories are local project infrastructure and are not committed to the repository.

## Development Environment

The project is developed on a Windows laptop using Visual Studio Code with WSL Ubuntu.

The development environment consists of:

- Windows
- Visual Studio Code
- WSL Ubuntu
- Python virtual environment
- Git for version control

The current Python environment uses Python 3.14.4.

## Setup Instructions

Run the following commands from the project root in WSL Ubuntu.

### 1. Create the virtual environment

```bash
python3 -m venv .venv
```

### 2. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The main runtime dependencies include Flask and Playwright. Pytest is used for automated testing.

If Pytest is not installed, run:

```bash
pip install pytest
```

### 4. Install Chromium

```bash
playwright install chromium
```

If browser system dependencies are required on WSL/Linux, run:

```bash
playwright install-deps chromium
```

## Running the Local Applications

Keep both applications running in separate terminals.

### Terminal 1 — Invoice Portal

```bash
cd /home/praneeth_reddy/projects/centrAlign-taskpilot
source .venv/bin/activate
python src/environment/invoice_portal.py
```

The application should be available at:

`http://127.0.0.1:8000`

### Terminal 2 — Finance System

```bash
cd /home/praneeth_reddy/projects/centrAlign-taskpilot
source .venv/bin/activate
python src/environment/finance_app.py
```

The application should be available at:

`http://127.0.0.1:8001`

Keep both terminals running while executing the agent and integration tests.

## Running TaskPilot

Open a third terminal and run:

```bash
cd /home/praneeth_reddy/projects/centrAlign-taskpilot
source .venv/bin/activate
python src/main.py
```

The current demonstration task is:

`Process invoice INV-1042`

A successful run reports the task, execution plan, final agent state, state history, invoice details, finance-system result, verification result, and completed steps.

The final success message is:

`TASKPILOT: TASK COMPLETED SUCCESSFULLY`

## Running Automated Tests

The project uses Pytest, configured through `pytest.ini`. The configuration adds the `src` directory to the Python import path.

Run the complete test suite with:

```bash
pytest -v
```

The current suite contains 24 tests covering:

- Task understanding
- Plan creation
- Invoice lookup
- Missing-invoice behavior
- Presence of the verification step
- Initial agent state
- State transitions during planning
- Empty task rejection
- Rejection of task changes after planning
- Missing invoice number handling
- Prevention of repeated execution after failure
- Valid and invalid state transitions
- Terminal-state behavior
- Recovery after a transient lookup error
- Stopping after the retry limit
- Avoiding retries for missing invoices
- Agent failure after lookup errors
- Failure when the Finance System rejects a save
- Failure when independent verification returns false
- Failure when independent verification raises an exception

**Latest verified test result: 24 passed.**

Run the tests again after making changes to confirm that the suite still passes.

## Development Progress

### Day 1 — Execution Environment

Completed:

- WSL and Python environment setup
- Git repository initialization
- Project structure creation
- Flask Invoice Portal
- Flask Finance System
- Playwright browser automation
- Structured invoice extraction
- Invoice submission
- Independent verification

### Day 2 — Agent Workflow

Completed:

- TaskPilot agent layer
- Task understanding
- Four-step task planning
- Browser tool integration
- Invoice lookup
- Finance tool integration
- Independent verification integration
- End-to-end INV-1042 workflow
- Pytest configuration and initial agent tests

### Day 3 — State Management and Recovery

Implemented:

- Explicit agent lifecycle states
- Validated state transitions
- State-history tracking
- Input validation
- Invoice-number extraction using a regular expression
- Failure reporting
- Protection against repeated execution after a terminal result
- Bounded invoice lookup retries
- Recovery-attempt logging
- Dedicated state-management tests
- Dedicated recovery tests
- State-history output in `src/main.py`

At the end of Day 3, the test suite contained 21 passing tests.


### Day 4 — Failure-Path Testing

Completed:

- Isolated invoice lookup unit tests from the live Invoice Portal
- Added tests for finance-save rejection
- Added tests for unsuccessful independent verification
- Added tests for exceptions raised during verification
- Confirmed that failed operations leave the agent in the `FAILED` state
- Confirmed that verification is not recorded as completed when it fails
- Verified the complete test suite: 24 passing tests

## Current Limitations

The current agent is a deterministic prototype and does not yet use an LLM for dynamic reasoning or planning.

The task execution is still focused on invoice processing. Invoice-number extraction uses a defined pattern, and the agent does not yet select tools dynamically for arbitrary business tasks.

Recovery is limited to invoice lookup. Finance submission and verification are not automatically retried.

The prototype uses local simulated applications and is not designed for production finance systems.

## Next Development Goals

Potential future improvements include:

- Observation-driven next-action selection
- More comprehensive failure detection
- Safer recovery for additional failure types
- Stronger verification and evidence collection
- Support for multiple task types
- Improved execution logging
- More comprehensive end-to-end tests
- Agent evaluation
- Human approval for sensitive operations
- A demonstration interface
- LLM-based reasoning and planning when they provide a concrete benefit

## Design Principles

### Separation of Reasoning and Execution

The agent coordinates the task while deterministic tools perform actual computer interactions.

### Observation

The agent should use observed results to determine whether an operation succeeded instead of assuming success.

### Verification

Successful execution and successful task completion are different concepts. The final outcome must be checked independently.

### Controlled Recovery

Retries should be bounded and appropriate to the operation. Side-effecting operations must not be repeated blindly.

### Controlled Environment

The prototype uses local simulated company applications rather than real company systems or credentials.

### Security

No real company credentials are required for the current demonstration. Future API keys and secrets should be stored in environment variables and excluded from Git.

## Git History

The existing development history includes:

- `8d69565` — Initial project setup
- `c9e25fd` — Day 1: build browser automation and verification
- `5a029d7` — Implement TaskPilot agent workflow and tests
- `528f7f4` — Update README with Day 2 agent workflow
- `0116d83` — Add agent state management and bounded recovery

The Day 3 changes were committed as `0116d83` — Add agent state management and bounded recovery.

## Project Goal

The long-term goal of CentrAlign TaskPilot is to demonstrate a reliable autonomous AI worker that can accept a natural-language business objective, plan the required actions, operate available tools, observe the results, recover safely from failures, verify the final outcome, and report completion.