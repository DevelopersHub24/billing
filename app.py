from flask import Flask
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔹 Secret key for session management
app.secret_key = "your_secret_key"

# 🔹 MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kamal$@1523'
app.config['MYSQL_DB'] = 'billing'

# 🔹 Initialize MySQL
mysql = MySQL(app)

# 🔹 SQLAlchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///purchase_bill.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 🔹 Import routes and models
from routes import *
from models import *

# 🔹 Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)