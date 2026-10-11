from environment.finance_app import app, saved_invoices


def test_duplicate_invoice_submission_is_rejected():
    saved_invoices.clear()
    client=app.test_client()

    data={
        "company":"Acme Corp",
        "invoice":"INV-1042",
        "amount":"48500",
        "due_date":"2026-10-20"
    }

    try:
        first=client.post("/",data=data)
        second=client.post("/",data={**data,"invoice":" inv-1042 "})

        assert b"Invoice saved successfully" in first.data
        assert b"Invoice already exists" in second.data
        assert len(saved_invoices)==1
    finally:
        saved_invoices.clear()
