from flask import Flask,request,render_template_string

app=Flask(__name__)

saved_invoices=[]

HTML="""
<!DOCTYPE html>
<html>
<head>
    <title>Finance System</title>
</head>
<body>
    <h1>Company Finance System</h1>

    <h2>Enter Invoice</h2>

    <form method="POST">

        <label>Company:</label>
        <input name="company" id="company">
        <br><br>

        <label>Invoice Number:</label>
        <input name="invoice" id="invoice">
        <br><br>

        <label>Amount:</label>
        <input name="amount" id="amount">
        <br><br>

        <label>Due Date:</label>
        <input name="due_date" id="due_date">
        <br><br>

        <button type="submit" id="save">Save Invoice</button>

    </form>

    {% if message %}
        <h3 id="message">{{ message }}</h3>
    {% endif %}

    <h2>Saved Invoices</h2>

    <table border="1" cellpadding="10">
        <tr>
            <th>Company</th>
            <th>Invoice</th>
            <th>Amount</th>
            <th>Due Date</th>
        </tr>

        {% for invoice in invoices %}
        <tr>
            <td>{{ invoice.company }}</td>
            <td>{{ invoice.invoice }}</td>
            <td>{{ invoice.amount }}</td>
            <td>{{ invoice.due_date }}</td>
        </tr>
        {% endfor %}

    </table>

</body>
</html>
"""

@app.route("/",methods=["GET","POST"])
def finance():

    message=""

    if request.method=="POST":

        invoice={
            "company":request.form["company"],
            "invoice":request.form["invoice"],
            "amount":request.form["amount"],
            "due_date":request.form["due_date"]
        }

        invoice_number=invoice["invoice"].strip().upper()

        if any(
            existing["invoice"].strip().upper()==invoice_number
            for existing in saved_invoices
        ):
            message="Invoice already exists"
        else:
            saved_invoices.append(invoice)
            message="Invoice saved successfully"

    return render_template_string(
        HTML,
        invoices=saved_invoices,
        message=message
    )

if __name__=="__main__":
    app.run(port=8001,debug=True)