# app.py
import os
from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL configurations
db_config = {
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'port': int(os.environ.get('DB_PORT'))
}

# Connect to the database
def connect_to_database():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Check database connection
db_connection = connect_to_database()

@app.route('/')
def index():
    if db_connection:
        # Fetch user data from the database
        cursor = db_connection.cursor()
        cursor.execute("SELECT Username, Password FROM user")
        users = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('index.html', users=users, db_connected=True)
    else:
        return render_template('index.html', db_connected=False)


