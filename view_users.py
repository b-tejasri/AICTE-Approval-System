import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))

cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

print("Users in DB:")
for row in rows:
    print(row)

conn.close()
