# CentrAlign TaskPilot

An autonomous AI task worker prototype inspired by the CentrAlign AI Engineering Hiring challenge.

## About the Project

CentrAlign TaskPilot is a prototype of an autonomous AI task worker designed to understand a user's goal, interact with computer-based tools, execute work, observe the results, recover from failures, verify the outcome, and report completion.

The prototype currently focuses on a narrow invoice-processing workflow in a controlled local company environment.

The current demonstration workflow is:

"Find the latest invoice from Acme Corp, extract the invoice information, enter it into the company finance system, and verify that it was saved."

The project is intentionally being developed as a narrow working prototype rather than attempting to support every possible website or company workflow.

## Current Architecture

The intended autonomous workflow is:

Goal
  ↓
Understand
  ↓
Plan
  ↓
Select Tool
  ↓
Execute
  ↓
Observe
  ↓
Adapt
  ↓
Verify
  ↓
Complete

The current implementation separates the agent layer from the deterministic computer-interaction tools.

The current architecture is:

User Goal
    ↓
TaskPilot Agent
    ↓
Browser Tool
    ↓
Invoice Portal
    ↓
Extract Invoice Data
    ↓
Finance Tool
    ↓
Finance System
    ↓
Independent Verifier
    ↓
Verified Result

The main engineering principle is to separate reasoning from execution.

The current TaskPilot agent is responsible for:

- Understanding the requested task
- Creating a task plan
- Calling the appropriate tools
- Passing data between tools
- Checking whether each major operation succeeded
- Returning the final task status

The deterministic tools are responsible for actually interacting with the computer environment.

The verification layer independently determines whether the requested outcome was achieved.

## Current Prototype Environment

The prototype contains two local web applications.

### 1. Invoice Portal

The Invoice Portal contains multiple company invoices.

It runs on:

http://127.0.0.1:8000

The current sample data contains invoices from:

- Acme Corp
- Beta Industries
- Gamma Solutions

There are multiple Acme Corp invoices so that the agent will eventually need to determine which invoice is the latest rather than simply using a hard-coded invoice.

The current latest Acme Corp invoice is:

Company: Acme Corp
Invoice: INV-1042
Date: 2026-10-05
Amount: 48500
Due Date: 2026-10-20

### 2. Finance System

The Finance System provides a form for entering invoice information.

It runs on:

http://127.0.0.1:8001

The form contains:

- Company
- Invoice Number
- Amount
- Due Date
- Save Invoice

After submission, the invoice appears in the Saved Invoices table.

## Current Browser Automation

Playwright is used for browser automation.

The browser automation layer can currently:

1. Open the Invoice Portal.
2. Read invoice information from the webpage.
3. Convert the observed invoice information into structured Python data.
4. Open the Finance System.
5. Fill the invoice form.
6. Submit the invoice.
7. Observe the result.

Chromium is used as the browser controlled by Playwright.

## Current Agent Layer

The TaskPilot agent is implemented in:

src/agent/agent.py

The agent currently provides the following operations:

### Understand

The agent receives a natural-language task such as:

"Process invoice INV-1042"

and stores the task as the current goal.

### Plan

The agent creates a four-step execution plan:

1. Find the requested invoice
2. Extract invoice details
3. Enter invoice details into the finance system
4. Verify the saved invoice

### Find Invoice

The agent calls the Browser Tool to retrieve invoices from the Invoice Portal.

It then searches the structured invoice data for the requested invoice number.

For example:

INV-1042

is resolved to:

Company: Acme Corp
Invoice: INV-1042
Date: 2026-10-05
Amount: 48500
Due Date: 2026-10-20

### Execute

The agent passes the discovered invoice to the Finance Tool.

The Finance Tool opens the Finance System, fills the form, submits the invoice, and returns the observed result.

### Verify

After the invoice is submitted, the agent calls the independent verification layer.

The verifier checks the actual saved invoice rather than trusting only the Finance System success message.

## Current Finance Tool

The finance tool is implemented in:

src/tools/finance_tool.py

The finance tool uses Playwright to:

1. Open the Finance System.
2. Fill the company field.
3. Fill the invoice number.
4. Fill the amount.
5. Fill the due date.
6. Click Save Invoice.
7. Observe the result.

The current demonstration submits:

Company: Acme Corp
Invoice: INV-1042
Amount: 48500
Due Date: 2026-10-20

## Current Verification

The verification layer is implemented in:

src/verification/verifier.py

The verification layer independently checks the Finance System after execution.

It verifies:

- Company
- Invoice Number
- Amount
- Due Date

The current verification workflow does not simply trust the success message returned by the application.

Instead, it opens the Finance System and checks whether the expected invoice actually exists in the Saved Invoices table.

A successful verification produces:

VERIFICATION: Invoice successfully verified

## Current End-to-End Capability

The current TaskPilot workflow is:

User Task
    ↓
TaskPilotAgent
    ↓
Understand Task
    ↓
Create Plan
    ↓
Browser Tool
    ↓
Invoice Portal
    ↓
Find Requested Invoice
    ↓
Extract Invoice Data
    ↓
Finance Tool
    ↓
Finance System
    ↓
Save Invoice
    ↓
Independent Verifier
    ↓
Verify Saved Invoice
    ↓
Task Completed Successfully

The current demonstration task is:

Process invoice INV-1042

A successful execution produces:

TASKPILOT: TASK COMPLETED SUCCESSFULLY

## Project Structure

centrAlign-taskpilot/
│
├── src/
│   ├── agent/
│   │   └── agent.py
│   │
│   ├── environment/
│   │   ├── invoice_portal.py
│   │   └── finance_app.py
│   │
│   ├── tools/
│   │   ├── browser.py
│   │   └── finance_tool.py
│   │
│   ├── verification/
│   │   └── verifier.py
│   │
│   └── main.py
│
├── tests/
│   └── test_agent.py
│
├── data/
│
├── .venv/
│
├── .git/
│
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt

The .venv and .git directories are local/project infrastructure and are not committed to the repository.

## Development Environment

The project is developed on Windows using Visual Studio Code with WSL Ubuntu as the runtime environment.

The development setup is:

Windows
  ↓
Visual Studio Code
  ↓
WSL Ubuntu
  ↓
Python Virtual Environment
  ↓
CentrAlign TaskPilot

VS Code is used as the primary development environment.

WSL Ubuntu is used to run Python and the project dependencies.

Git is used for version control.

## Python Environment Setup

Create the project virtual environment with:

python3 -m venv .venv

Activate the virtual environment with:

source .venv/bin/activate

The project currently uses Python 3.14.4.

The expected Python executable inside the project is:

/home/praneeth_reddy/projects/centrAlign-taskpilot/.venv/bin/python

## Installing Dependencies

Activate the virtual environment first:

source .venv/bin/activate

Install the project dependencies:

pip install -r requirements.txt

The main runtime requirements are:

Flask==3.1.3
playwright==1.63.0

Pytest is also used for automated testing.

Install Pytest with:

pip install pytest

Install the Playwright Chromium browser:

playwright install chromium

On WSL/Linux, if browser system dependencies are required, run:

playwright install-deps chromium

## Running the Local Environment

The local environment requires the Invoice Portal and Finance System to be running.

### Start the Invoice Portal

Run:

python src/environment/invoice_portal.py

The Invoice Portal will be available at:

http://127.0.0.1:8000

Keep this terminal running.

### Start the Finance System

Open another terminal.

Activate the virtual environment:

source .venv/bin/activate

Then run:

python src/environment/finance_app.py

The Finance System will be available at:

http://127.0.0.1:8001

Keep this terminal running.

## Running the Browser Tool

Open another terminal and activate the virtual environment.

Run:

python src/tools/browser.py

The browser tool uses Playwright to open the Invoice Portal and extract invoice information.

The result is converted into structured data containing:

- company
- invoice
- date
- amount
- due_date

## Running the Finance Tool

Run:

python src/tools/finance_tool.py

The finance tool uses Playwright to:

1. Open the Finance System.
2. Fill the company field.
3. Fill the invoice number.
4. Fill the amount.
5. Fill the due date.
6. Click Save Invoice.
7. Observe the result.

## Running the Verifier

Run:

python src/verification/verifier.py

The verifier opens the Finance System and independently checks whether the expected invoice exists.

A successful verification produces:

VERIFICATION: Invoice successfully verified

## Running TaskPilot

Make sure both local applications are running:

Terminal 1:

python src/environment/invoice_portal.py

Terminal 2:

python src/environment/finance_app.py

Then run the TaskPilot agent from another terminal:

python src/main.py

The current demonstration task is:

Process invoice INV-1042

A successful run performs the complete workflow:

1. Understand the task.
2. Create an execution plan.
3. Find INV-1042 using the Browser Tool.
4. Extract the invoice information.
5. Save the invoice using the Finance Tool.
6. Verify the saved invoice independently.
7. Report successful completion.

## Automated Testing

The project uses Pytest.

Pytest is configured through:

pytest.ini

The configuration adds the src directory to the Python import path.

Run all tests with:

pytest

The current test suite contains five tests.

The tests currently verify:

1. The agent understands the requested task.
2. The agent creates the expected execution plan.
3. The agent can find INV-1042.
4. The agent correctly handles a missing invoice.
5. The agent plan contains the verification step.

Current test result:

5 passed

## Testing Philosophy

Testing is being added alongside the agent implementation rather than only testing the final application.

The project currently tests both normal behavior and basic failure behavior.

The next testing stages will cover:

- Finance tool failure
- Verification failure
- Browser failures
- Recovery behavior
- End-to-end execution
- Multiple invoice scenarios

## Current Status

### Day 1 — Execution Environment

Completed:

- Windows development environment configured
- WSL Ubuntu configured
- VS Code connected to WSL
- Python 3.14.4 configured
- Python virtual environment created
- Git repository initialized
- Main Git branch configured
- Project structure created
- Flask installed
- Playwright installed
- Chromium installed
- Playwright Linux dependencies installed
- Local Invoice Portal implemented
- Local Finance System implemented
- Browser observation implemented
- Structured invoice extraction implemented
- Browser execution implemented
- Invoice submission implemented
- Independent verification implemented

### Day 2 — Agent Workflow

Completed:

- TaskPilot agent layer created
- Task understanding implemented
- Task planning implemented
- Browser Tool connected to the agent
- Invoice lookup implemented
- Finance Tool connected to the agent
- Invoice submission integrated into the agent workflow
- Independent verification integrated into the agent workflow
- End-to-end INV-1042 workflow successfully executed
- Pytest configured
- Automated agent tests created
- Five automated tests passing
- Day 2 changes committed to Git

Current Day 2 Git commit:

Implement TaskPilot agent workflow and tests

## Current Limitations

The current agent is a deterministic prototype.

It does not yet use an LLM for dynamic reasoning or planning.

The invoice number is currently derived from the task format:

Process invoice INV-1042

The current implementation therefore demonstrates the architecture and execution flow but does not yet provide general-purpose autonomous task planning.

The recovery logic is also still limited.

The next stage will make the agent more adaptive and observation-driven.

## Next Development Stage

The next development stage is to move from the current deterministic agent toward a more autonomous task worker.

Planned improvements include:

- LLM-based task understanding
- LLM-based planning
- Dynamic tool selection
- Agent state management
- Observation-driven next actions
- Failure detection
- Retry and recovery
- Human approval when required
- Stronger verification
- Evidence collection
- Support for multiple task types
- Agent evaluation
- Improved logging
- Better error handling
- Demo interface
- More comprehensive automated tests

## Target Autonomous Architecture

The target architecture is:

User
  ↓
Natural Language Goal
  ↓
Agent
  ↓
Understand
  ↓
Plan
  ↓
Select Tool
  ↓
Execute
  ↓
Observe
  ↓
Reason
  ↓
Adapt or Continue
  ↓
Verify
  ↓
Evidence
  ↓
Complete

The deterministic tools will remain responsible for actual computer interaction.

The future agent will be responsible for deciding what action should happen next based on the goal and observations.

## Design Principles

### Separation of Reasoning and Execution

The agent should decide what action is required and select an appropriate tool.

The tool performs the actual operation.

This prevents the reasoning layer from directly performing arbitrary computer operations.

### Observation

After an action, the agent should receive information about what actually happened.

The agent should use the observation to determine the next action rather than assuming that an action succeeded.

### Verification

Successful execution and successful completion are treated as different concepts.

An action can appear to succeed while the requested outcome is still not achieved.

The verification layer therefore independently checks the final state.

### Recovery

If an action fails or the environment is different from what was expected, the future agent should detect the failure and attempt a reasonable alternative or retry when appropriate.

### Controlled Environment

The prototype uses a local simulated company environment rather than real company systems or credentials.

This provides a safe environment for demonstrating autonomous computer interaction.

## Security

No real company credentials or confidential information are used.

The prototype uses local simulated applications.

Future API keys and secrets will be stored in environment variables and excluded from Git using .gitignore.

## Git History

The current development history includes:

Day 1:

Day 1: build browser automation and verification

Day 2:

Implement TaskPilot agent workflow and tests

The working tree is kept clean after completed development milestones.

## Project Goal

The long-term goal of CentrAlign TaskPilot is to demonstrate a reliable autonomous AI worker that can take a natural-language business objective, determine what needs to be done, operate available computer tools, adapt to changing results, verify the outcome, and provide useful evidence of completion.