
import logging
import re
import uuid
from datetime import datetime, timezone

from tools.browser import get_invoices
from tools.finance_tool import save_invoice
from verification.verifier import verify_invoice
from agent.state import AgentState, transition
from observability import get_logger, log_event

class TaskPilotAgent:

    def __init__(self):
        self.logger=get_logger('taskpilot.agent')
        self.execution_id=str(uuid.uuid4())
        self.started_at=datetime.now(timezone.utc).isoformat()
        self.execution_history=[]
        self.task=None
        self.plan=[]
        self.completed_steps=[]
        self.invoice=None
        self.state=AgentState.IDLE
        self.state_history=[]
        self.error=None
        self._last_result=None
        self.recovery_history=[]
        self.lookup_attempts=0


    def _record_audit_event(self,event,**details):
        timestamp=datetime.now(timezone.utc).isoformat()

        record={
            "execution_id":self.execution_id,
            "timestamp":timestamp,
            "event":event
        }
        record.update(details)
        self.execution_history.append(record)

        log_event(
            self.logger,
            logging.INFO,
            "audit_event",
            **{
                "execution_id":self.execution_id,
                "timestamp":timestamp,
                "audit_event":event,
                **details
            }
        )


    def _set_state(self,next_state):
        previous_state=self.state
        self.state=transition(self.state,next_state)

        transition_record={
            "from":previous_state.value,
            "to":self.state.value
        }
        self.state_history.append(transition_record)

        self._record_audit_event(
            "state_transition",
            previous_state=previous_state.value,
            next_state=self.state.value
        )

        log_event(
            self.logger,
            logging.INFO,
            "state_transition",
            execution_id=self.execution_id,
            previous_state=previous_state.value,
            next_state=self.state.value
        )



    def _fail(self,message):
        self.error=message

        if self.state not in (AgentState.FAILED,AgentState.COMPLETED):
            self._set_state(AgentState.FAILED)

        self._last_result={
            "status":"failed",
            "error":message,
            "state":self.state.value
        }

        self._record_audit_event(
            "execution_finished",
            status="failed",
            failure_reason=message,
            final_state=self.state.value
        )

        log_event(
            self.logger,
            logging.ERROR,
            "execution_failed",
            execution_id=self.execution_id,
            reason=message,
            state=self.state.value
        )

        return self._last_result


    def understand(self,task):
        if self.state!=AgentState.IDLE:
            raise ValueError("This agent has already started a task")

        if not isinstance(task,str) or not task.strip():
            raise ValueError("Task must be a non-empty string")

        self.task=task.strip()

        return {
            "goal":self.task,
            "status":"understood"
        }

    def create_plan(self):
        if self.state==AgentState.READY:
            return self.plan

        if self.state!=AgentState.IDLE:
            raise ValueError(
                f"Cannot create a plan while agent is {self.state.value}"
            )

        self._set_state(AgentState.PLANNING)

        self.plan=[
            "Find the requested invoice",
            "Extract invoice details",
            "Enter invoice details into the finance system",
            "Verify the saved invoice"
        ]

        self._set_state(AgentState.READY)

        return self.plan

    def find_invoice(self,invoice_number):
        invoices=get_invoices()

        for invoice in invoices:
            if invoice["invoice"]==invoice_number:
                self.invoice=invoice
                return invoice

        return None


    def _find_invoice_with_retry(self,invoice_number,max_attempts=2):
        for attempt in range(1,max_attempts+1):
            self.lookup_attempts=attempt

            try:
                invoice=self.find_invoice(invoice_number)

                self.recovery_history.append({
                    "operation":"find_invoice",
                    "attempt":attempt,
                    "status":"found" if invoice is not None else "not_found"
                })

                return invoice

            except Exception as exc:
                self.recovery_history.append({
                    "operation":"find_invoice",
                    "attempt":attempt,
                    "status":"error",
                    "error":f"{type(exc).__name__}: {exc}"
                })

                if attempt==max_attempts:
                    raise

        return None


    def execute(self):
        if self.state==AgentState.COMPLETED:
            return self._last_result

        if self.state==AgentState.FAILED:
            return self._last_result

        if not self.task:
            return self._fail("No task has been provided")

        if self.state==AgentState.IDLE:
            self.create_plan()

        match=re.search(r"\bINV-\d+\b",self.task,re.IGNORECASE)

        if match is None:
            return self._fail(
                "Could not identify an invoice number in the task"
            )

        invoice_number=match.group().upper()


        self._record_audit_event(
            "execution_started",
            invoice_number=invoice_number,
            started_at=self.started_at
        )

        log_event(
            self.logger,
            logging.INFO,
            "execution_started",
            execution_id=self.execution_id,
            invoice_number=invoice_number
        )

        self._set_state(AgentState.RUNNING)


        try:
            invoice=self._find_invoice_with_retry(invoice_number)

            if invoice is None:
                return self._fail(
                    f"Invoice {invoice_number} not found"
                )

            self.completed_steps.append(
                "Find the requested invoice"
            )
            self.completed_steps.append(
                "Extract invoice details"
            )

            message=save_invoice(invoice)

            if message!="Invoice saved successfully":
                return self._fail(
                    "Invoice could not be saved"
                )

            self.completed_steps.append(
                "Enter invoice details into the finance system"
            )

            self._set_state(AgentState.VERIFYING)

            verified=verify_invoice(invoice)

            if not verified:
                return self._fail(
                    "Invoice verification failed"
                )

            self.completed_steps.append(
                "Verify the saved invoice"
            )


            self._set_state(AgentState.COMPLETED)

            self._last_result={
                "status":"completed",
                "invoice":invoice,
                "finance_message":message,
                "verified":True,
                "completed_steps":self.completed_steps.copy(),
                "state":self.state.value
            }

            self._record_audit_event(
                "execution_finished",
                status="completed",
                final_state=self.state.value,
                verified=True,
                completed_steps=self.completed_steps.copy()
            )

            return self._last_result


        except Exception as exc:
            return self._fail(
                f"Execution error: {type(exc).__name__}: {exc}"
            )
