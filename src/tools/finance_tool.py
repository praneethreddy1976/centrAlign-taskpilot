from playwright.sync_api import sync_playwright

def save_invoice(invoice):
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page()

        page.goto("http://127.0.0.1:8001")

        page.locator("#company").fill(invoice["company"])
        page.locator("#invoice").fill(invoice["invoice"])
        page.locator("#amount").fill(str(invoice["amount"]))
        page.locator("#due_date").fill(invoice["due_date"])

        page.locator("#save").click()

        message=page.locator("#message").inner_text()

        print("Finance system:",message)

        browser.close()

        return message

if __name__=="__main__":
    invoice={
        "company":"Acme Corp",
        "invoice":"INV-1042",
        "amount":48500,
        "due_date":"2026-10-20"
    }

    save_invoice(invoice)