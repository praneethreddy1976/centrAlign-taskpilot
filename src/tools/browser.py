from playwright.sync_api import sync_playwright

def get_invoices():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page()

        page.goto("http://127.0.0.1:8000")

        rows=page.locator("table tr")

        invoices=[]

        for i in range(1,rows.count()):
            cells=rows.nth(i).locator("td").all_inner_texts()

            invoices.append({
                "company":cells[0],
                "invoice":cells[1],
                "date":cells[2],
                "amount":int(cells[3]),
                "due_date":cells[4]
            })

        browser.close()

        return invoices

if __name__=="__main__":
    invoices=get_invoices()

    for invoice in invoices:
        print(invoice)