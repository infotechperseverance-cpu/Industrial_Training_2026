import sqlite3
import datetime
import os

# 1. Database connect
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# 2. Table banav
cursor.execute('''CREATE TABLE IF NOT EXISTS file_log
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   file_name TEXT, 
                   action TEXT, 
                   content TEXT, 
                   time TEXT)''')
conn.commit()

# 3. DB madhe save karnyacha function
def save_to_db(filename, action, content):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO file_log (file_name, action, content, time) VALUES (?, ?, ?, ?)",
                   (filename, action, content, time_now))  # <-- 4 ? aahet ithe
    conn.commit()
    print(f"DB me save: {action} on {filename}")

# 4. File Handling Functions
def write_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    save_to_db(filename, "write", data)

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()
    save_to_db(filename, "read", data)
    return data

def append_file(filename, data):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(data + "\n")
    save_to_db(filename, "append", data)

# 5. Test karnyasathi
if __name__ == "__main__":
    append_file("notes.txt", "Hello from file handling")
    append_file("notes.txt", "Second line added")
    content = read_file("notes.txt")
    print("\nFile Content:")
    print(content)
    conn.close()
    print("\nDone! Check tasks.db and notes.txt")