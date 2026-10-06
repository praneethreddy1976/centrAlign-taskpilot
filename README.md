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

The current implementation has already established the execution environment required for this agent loop.

The current architecture is:

User Goal
    ↓
Agent Layer
    ↓
Tool Selection
    ↓
Browser Tools
    ↓
Local Company Applications
    ↓
Observation
    ↓
Verification
    ↓
Result

The main engineering principle is to separate reasoning from execution.

The future LLM agent will be responsible for understanding the task, planning actions, selecting tools, and deciding what to do next.

The tools will be responsible for actually interacting with the computer environment.

The verification layer will independently determine whether the requested outcome was achieved.

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

## Current Verification

The verification layer independently checks the Finance System after execution.

It verifies:

- Company
- Invoice Number
- Amount
- Due Date

The current verification workflow does not simply trust the success message returned by the application.

Instead, it opens the Finance System and checks whether the expected invoice actually exists in the Saved Invoices table.

## Project Structure

centrAlign-taskpilot/
│
├── src/
│   ├── agent/
│   │   └──
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
│
├── data/
│
├── .venv/
│
├── .git/
│
├── .gitignore
│
├── README.md
│
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

The current requirements are:

Flask==3.1.3
playwright==1.63.0

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

## Running Browser Observation

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

## Running Browser Execution

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

The current demonstration submits:

Company: Acme Corp
Invoice: INV-1042
Amount: 48500
Due Date: 2026-10-20

## Running Verification

Run:

python src/verification/verifier.py

The verifier opens the Finance System and independently checks whether the expected invoice exists.

A successful verification produces:

VERIFICATION: Invoice successfully verified

## Current End-to-End Capability

The current deterministic workflow is:

Invoice Portal
    ↓
Playwright
    ↓
Read invoice information
    ↓
Finance Tool
    ↓
Open Finance System
    ↓
Fill invoice information
    ↓
Submit invoice
    ↓
Verification
    ↓
Confirm saved invoice

The browser automation and verification components have been tested successfully in the WSL environment.

## Current Status

Day 1 is focused on building the reliable execution environment before introducing the autonomous LLM agent.

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

## Next Development Stage

The next stage is to introduce the autonomous agent layer.

The deterministic tools will remain responsible for actual computer interaction.

The LLM agent will be responsible for:

- Understanding the user's intended outcome
- Breaking the goal into actions
- Planning the task
- Selecting appropriate tools
- Interpreting observations
- Deciding the next action
- Handling failures
- Attempting reasonable recovery
- Maintaining task state
- Requesting human input when required
- Deciding when verification should occur

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

## Design Principles

### Separation of Reasoning and Execution

The LLM should not directly perform arbitrary system operations.

The LLM should decide what action is required and select an appropriate tool.

The tool performs the actual operation.

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

## Future Improvements

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
- Comprehensive automated tests

## Project Goal

The long-term goal of CentrAlign TaskPilot is to demonstrate a reliable autonomous AI worker that can take a natural-language business objective, determine what needs to be done, operate available computer tools, adapt to changing results, verify the outcome, and provide useful evidence of completion.