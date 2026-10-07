from tools.browser import get_invoices
from tools.finance_tool import save_invoice
from verification.verifier import verify_invoice


class TaskPilotAgent:

    def __init__(self):
        self.task=None
        self.plan=[]
        self.completed_steps=[]
        self.invoice=None

    def understand(self,task):
        self.task=task

        return {
            "goal":task,
            "status":"understood"
        }

    def create_plan(self):
        self.plan=[
            "Find the requested invoice",
            "Extract invoice details",
            "Enter invoice details into the finance system",
            "Verify the saved invoice"
        ]

        return self.plan

    def find_invoice(self,invoice_number):
        invoices=get_invoices()

        for invoice in invoices:
            if invoice["invoice"]==invoice_number:
                self.invoice=invoice
                return invoice

        return None

    def execute(self):
        invoice_number=self.task.split()[-1]

        invoice=self.find_invoice(invoice_number)

        if invoice is None:
            return {
                "status":"failed",
                "error":f"Invoice {invoice_number} not found"
            }

        self.completed_steps.append("Find the requested invoice")
        self.completed_steps.append("Extract invoice details")

        message=save_invoice(invoice)

        if message!="Invoice saved successfully":
            return {
                "status":"failed",
                "error":"Invoice could not be saved"
            }

        self.completed_steps.append("Enter invoice details into the finance system")
        verified=verify_invoice(invoice)

        if not verified:
           return {
              "status":"failed",
               "error":"Invoice verification failed"
            }

        self.completed_steps.append("Verify the saved invoice")
        
        return {
            "status":"completed",
            "invoice":invoice,
            "finance_message":message,
            "verified":True,
            "completed_steps":self.completed_steps
        }