from flask import render_template, request, jsonify, redirect, url_for, session, flash
from app import app, db
from models import Supplier, Item, PurchaseBill, PurchaseBillItem
from helpers import generate_bill_number
from datetime import datetime
from app import app, mysql
import MySQLdb.cursors  # Import MySQLdb for DictCursor

# 🔹 Home Route (Login Page)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM AdminMaster WHERE admin_userid = %s", (userid,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            # 🔹 Ensure the key matches the database column name correctly
            if password == user.get('password'):  # Direct comparison, no hashing
                session['loggedin'] = True
                session['userid'] = user['admin_userid']
                session['name'] = user['name']
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))  # Redirect to dashboard
            else:
                flash("Invalid credentials!", "danger")
        else:
            flash("User not found!", "danger")

    return render_template("index.html")

# 🔹 Dashboard Route (After Login)
@app.route('/home/dashboard')
def dashboard():
    if 'loggedin' in session:
        return render_template("home/home.html", name=session['name'])
    return redirect(url_for('login'))

# 🔹 Sales Bill Route
@app.route('/home/billing/sales')
def sales_bill():
    if 'loggedin' in session:
        return render_template("billing_screens/sales.html", name=session['name'])
    return redirect(url_for('login'))

# 🔹 Inventory Route
@app.route('/home/inventory')
def inventory():
    if 'loggedin' in session:
        return render_template("home/inventory.html", name=session['name'])
    return redirect(url_for('login'))

@app.route('/home/billing/purchase')
def purchase_bill():
    if 'loggedin' in session:
        return render_template("billing_screens/purchase.html", name=session['name'])
    return redirect(url_for('login'))

@app.route('/home/billing/credit-note')
def credit_note():
    if 'loggedin' in session:
        return render_template("billing_screens/creditnote.html", name=session['name'])
    return redirect(url_for('login'))

@app.route('/home/billing/debit-note')
def debit_note():
    if 'loggedin' in session:
        return render_template("billing_screens/debitnote.html", name=session['name'])
    return redirect(url_for('login'))

@app.route('/home/billing/proforma')
def proforma_invoice():
    if 'loggedin' in session:
        return render_template("billing_screens/proforma.html", name=session['name'])
    return redirect(url_for('login'))

@app.route('/home/billing/asn')
def asn():
    if 'loggedin' in session:
        return render_template("billing_screens/asn.html", name=session['name'])
    return redirect(url_for('login'))

@app.route('/home/billing/delivery-challan')
def delivery_challan():
    if 'loggedin' in session:
        return render_template("billing_screens/delivery.html", name=session['name'])
    return redirect(url_for('login'))

@app.route('/home/billing/quotation')
def quotation():
    if 'loggedin' in session:
        return render_template("billing_screens/quotation.html", name=session['name'])
    return redirect(url_for('login'))

# 🔹 Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))