from playwright.sync_api import sync_playwright

def verify_invoice(invoice):
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page()

        page.goto("http://127.0.0.1:8001")

        rows=page.locator("table tr")

        for i in range(1,rows.count()):
            cells=rows.nth(i).locator("td").all_inner_texts()

            if len(cells)==4:
                company=cells[0]
                invoice_number=cells[1]
                amount=cells[2]
                due_date=cells[3]

                if(
                    company==invoice["company"]
                    and invoice_number==invoice["invoice"]
                    and amount==str(invoice["amount"])
                    and due_date==invoice["due_date"]
                ):
                    browser.close()
                    return True

        browser.close()
        return False

if __name__=="__main__":
    invoice={
        "company":"Acme Corp",
        "invoice":"INV-1042",
        "amount":48500,
        "due_date":"2026-10-20"
    }

    result=verify_invoice(invoice)

    if result:
        print("VERIFICATION: Invoice successfully verified")
    else:
        print("VERIFICATION: Invoice verification failed")