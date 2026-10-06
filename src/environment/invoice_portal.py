from flask import Flask,render_template_string

app=Flask(__name__)

HTML="""
<!DOCTYPE html>
<html>
<head>
    <title>Invoice Portal</title>
</head>
<body>
    <h1>Company Invoice Portal</h1>

    <h2>Invoices</h2>

    <table border="1" cellpadding="10">
        <tr>
            <th>Company</th>
            <th>Invoice</th>
            <th>Date</th>
            <th>Amount</th>
            <th>Due Date</th>
        </tr>

        <tr>
            <td>Acme Corp</td>
            <td>INV-1038</td>
            <td>2026-09-15</td>
            <td>31200</td>
            <td>2026-09-30</td>
        </tr>

        <tr>
            <td>Beta Industries</td>
            <td>INV-2041</td>
            <td>2026-10-01</td>
            <td>67500</td>
            <td>2026-10-15</td>
        </tr>

        <tr>
            <td>Acme Corp</td>
            <td>INV-1042</td>
            <td>2026-10-05</td>
            <td>48500</td>
            <td>2026-10-20</td>
        </tr>

        <tr>
            <td>Gamma Solutions</td>
            <td>INV-3012</td>
            <td>2026-10-03</td>
            <td>22100</td>
            <td>2026-10-18</td>
        </tr>
    </table>
</body>
</html>
"""

@app.route("/")
def invoices():
    return render_template_string(HTML)

if __name__=="__main__":
    app.run(port=8000,debug=True)