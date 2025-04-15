import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

def create_connection():
    """Creates and returns a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Change if using a different host
            user="root",       # Replace with your MySQL username
            password="",       # Replace with your MySQL password
            database="bank_management"  # Replace with your database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection

    except Error as e:
        print(f"Error connecting to MySQL: {e}")  # Print error for debugging
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        return None
