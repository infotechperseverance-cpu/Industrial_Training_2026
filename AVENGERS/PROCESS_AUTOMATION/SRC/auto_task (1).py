import sqlite3
import datetime

# Database connect
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS task_log
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   task_name TEXT, status TEXT, execution_time TEXT)''')
conn.commit()

def automatic_task(task_name):
    time_now = datetime.datetime.now()
    try:
        # Yethe tuzya automatic task cha code
        print(f"Running: {task_name}")
        
        # Success zalyavar DB madhe save
        cursor.execute("INSERT INTO task_log (task_name, status, execution_time) VALUES (?, ?, ?)",
                       (task_name, "Success", time_now))
    except Exception as e:
        cursor.execute("INSERT INTO task_log (task_name, status, execution_time) VALUES (?, ?, ?)",
                       (task_name, f"Failed: {e}", time_now))
    conn.commit()

# 3 different automatic tasks run kar
automatic_task("Data Backup")
automatic_task("Email Send")
automatic_task("Report Generate")

# Sagla data print kar
cursor.execute("SELECT * FROM task_log")
print("\nDatabase Records:")
for row in cursor.fetchall():
    print(row)

conn.close()