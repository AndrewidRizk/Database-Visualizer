# app.py
import os
import mysql.connector
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# MySQL configurations
db_config = {
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'port': 3306  # Default port is 3306
}

# Function to connect to the database with error handling and retry mechanism
def connect_to_database():
    attempts = 3
    for attempt in range(1, attempts + 1):
        try:
            conn = mysql.connector.connect(**db_config)
            return conn
        except mysql.connector.Error as err:
            print(f"Attempt {attempt} to connect to the database failed: {err}")
            if attempt == attempts:
                print(f"Unable to connect to the database after {attempts} attempts.")
                return None

# Check and establish database connection
db_connection = connect_to_database()

# Route to display users from the database
@app.route('/')
def index():
    global db_connection
    if db_connection:
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT Username, Password FROM user")
            users = cursor.fetchall()
            cursor.close()
            return render_template('index.html', users=users, db_connected=True)
        except mysql.connector.Error as err:
            print(f"Error while querying database: {err}")
            db_connection = connect_to_database()  # Attempt to reconnect
            return render_template('index.html', db_connected=False)
    else:
        return render_template('index.html', db_connected=False)

# Route to refresh the database connection
@app.route('/refresh')
def refresh():
    global db_connection
    db_connection = connect_to_database()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
