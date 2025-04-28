from flask import Flask
from flask_mysqldb import MySQL

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

# 🔹 Import routes
from routes import *

if __name__ == "__main__":
    app.run(debug=True)