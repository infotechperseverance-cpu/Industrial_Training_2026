import sqlite3

DB_NAME = "logs.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
                      (id INTEGER PRIMARY KEY,
                       time TEXT,
                       task TEXT,
                       status TEXT,
                       error TEXT)''')
    
    conn.commit()
    return conn, cursor