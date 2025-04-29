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
        return render_template("home/billingscreen.html", name=session['name'])
    return redirect(url_for('login'))

# 🔹 Inventory Route
@app.route('/home/inventory')
def inventory():
    if 'loggedin' in session:
        return render_template("home/inventory.html", name=session['name'])
    return redirect(url_for('login'))

# @app.route('/home/billing/purchase')
# def purchase_bill():
#     if 'loggedin' in session:
#         return render_template("home/purchase.html", name=session['name'])
#     return redirect(url_for('login'))

# 🔹 Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


@app.route('/home/billing/purchase', methods=['GET', 'POST'])
def purchase_bill():
    if request.method == 'POST':
        data = request.get_json()
        bill = PurchaseBill(
            bill_number=generate_bill_number(),
            supplier_id=data['supplier_id'],
            bill_date=datetime.strptime(data['bill_date'], '%Y-%m-%d').date(),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data['due_date'] else None,
            reference_number=data['reference_number'],
            payment_terms=data['payment_terms'],
            subtotal=data['subtotal'],
            total_discount=data['total_discount'],
            taxable_amount=data['taxable_amount'],
            cgst_amount=data['cgst_amount'],
            sgst_amount=data['sgst_amount'],
            shipping_charges=data['shipping_charges'],
            grand_total=data['grand_total'],
            shipping_info=data['shipping_info'],
            notes=data['notes'],
            status='pending'
        )
        db.session.add(bill)
        db.session.commit()

        for item in data['items']:
            bill_item = PurchaseBillItem(
                bill_id=bill.id,
                item_id=item['item_id'],
                name=item['name'],
                description=item.get('description', ''),
                quantity=item['quantity'],
                purchase_price=item['purchase_price'],
                discount_percent=item['discount_percent'],
                discount_amount=item['discount_amount'],
                taxable_value=item['taxable_value'],
                gst_rate=item['gst_rate'],
                cgst_amount=item['cgst_amount'],
                sgst_amount=item['sgst_amount'],
                total_amount=item['total_amount'],
                hsn_code=item.get('hsn_code', '')
            )
            db.session.add(bill_item)

        db.session.commit()
        return jsonify({'success': True, 'bill_id': bill.id, 'bill_number': bill.bill_number})

    suppliers = Supplier.query.all()
    items = Item.query.all()
    return render_template('home/purchase.html', 
                           suppliers=suppliers,
                           items=items,
                           bill_number=generate_bill_number(),
                           current_date=datetime.now().strftime('%Y-%m-%d'))