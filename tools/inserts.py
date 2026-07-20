import sqlite3
import json

conn = sqlite3.connect("app_database.db")
cursor = conn.cursor()

for i in range(1, 11):
    cursor.execute(f"INSERT INTO users (name) VALUES ('user[{i}]');")

cursor.execute("SELECT * FROM users;")
result = cursor.fetchall()
print(json.dumps(result, indent=4))
conn.commit()
conn.close()
