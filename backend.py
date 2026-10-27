import sqlite3
from datetime import date
import pandas as pd

DB_NAME = "complaints.db"


# Database connection
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# Create database table
def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
            )
        """)
        conn.commit()


# Fetch all complaints
def fetch_complaints():
    with get_connection() as conn:
        return pd.read_sql_query(
            """SELECT id, name, category, description, date, status
               FROM complaints ORDER BY id DESC""",
            conn
        )


# Add complaint
def add_complaint(name, category, description):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO complaints
               (name, category, description, date, status)
               VALUES (?, ?, ?, ?, ?)""",
            (name, category, description, date.today().isoformat(), "Pending")
        )
        conn.commit()


# Edit complaint details
def update_complaint(complaint_id, name, category, description):
    with get_connection() as conn:
        conn.execute(
            """UPDATE complaints
               SET name = ?, category = ?, description = ?
               WHERE id = ?""",
            (name, category, description, int(complaint_id))
        )
        conn.commit()


# Update complaint status
def update_complaint_status(complaint_id, status):
    with get_connection() as conn:
        conn.execute(
            "UPDATE complaints SET status = ? WHERE id = ?",
            (status, int(complaint_id))
        )
        conn.commit()


# Delete complaint
def delete_complaint(complaint_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM complaints WHERE id = ?",
            (int(complaint_id),)
        )
        conn.commit()


# Initialize database
initialize_database()