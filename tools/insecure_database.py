import sqlite3

def connect():
    conn = sqlite3.connect("users.db")
    return conn

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            phone TEXT
        );
    ''')

    conn.commit()
    conn.close()

def get_all_user():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users;
    ''')
    conn.commit()
    conn.close()

def insert_user(username, password):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{username}' AND age = '{password}';"
    print(f"[QUERY] = {query}")
    cursor.execute(query)
    resultado = cursor.fetchall()
    print(f"[RESULTADO] = {resultado}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    username = input("Ingresa tu username: ")
    password = input("Ingresa tu password: ")
    insert_user(username, password)
