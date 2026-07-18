import sqlite3
import datetime
import schedule
import time

# Database connect
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS schedule_log
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   task_name TEXT, schedule_time TEXT, last_run TEXT)''')
conn.commit()

def scheduled_task():
    time_now = datetime.datetime.now()
    cursor.execute("UPDATE schedule_log SET last_run = ? WHERE task_name = ?",
                   (time_now, "My Task"))
    conn.commit()
    print(f"Scheduled Task Ran at: {time_now}")

# Schedule set kar
schedule.every(10).seconds.do(scheduled_task)

# DB madhe schedule entry
cursor.execute("INSERT INTO schedule_log (task_name, schedule_time) VALUES (?, ?)",
               ("My Task", "Every 10 seconds"))
conn.commit()

print("Scheduler Started...")
while True:
    schedule.run_pending()
    time.sleep(1)