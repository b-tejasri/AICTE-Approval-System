import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
cursor = conn.cursor()

# ------------------
# Users table
# ------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# ------------------
# Institutions table
# ------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS institutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    institution_name TEXT NOT NULL,
    institute_type TEXT,
    institute_id TEXT,
    affiliating_university TEXT,
    year_of_establishment INTEGER,
    state TEXT,
    district TEXT,
    city TEXT,
    pin_code TEXT,
    category TEXT,
    official_email TEXT,
    phone TEXT,
    authorized_person TEXT,
    designation TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

print("Database and tables created successfully")
