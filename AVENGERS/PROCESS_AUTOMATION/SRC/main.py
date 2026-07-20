import sqlite3

# Connect to database
conn = sqlite3.connect("task_management.db")
cursor = conn.cursor()

# User Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('User','Admin')) NOT NULL
)
""")

# Task Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task_name TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    assigned_date DATE,
    due_date DATE,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")

# Notification Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")

conn.commit()

# Add User
def add_user(username, password, role):
    cursor.execute(
        "INSERT INTO users(username,password,role) VALUES(?,?,?)",
        (username, password, role)
    )
    conn.commit()
    print("User Added Successfully")

# Add Task
def add_task(user_id, task_name, assigned_date, due_date):
    cursor.execute(
        "INSERT INTO tasks(user_id,task_name,assigned_date,due_date) VALUES(?,?,?,?)",
        (user_id, task_name, assigned_date, due_date)
    )
    conn.commit()
    print("Task Added Successfully")

# Update Task Status
def update_status(task_id, status):
    cursor.execute(
        "UPDATE tasks SET status=? WHERE task_id=?",
        (status, task_id)
    )
    conn.commit()
    print("Task Updated")

# Send Notification
def send_notification(user_id, message):
    cursor.execute(
        "INSERT INTO notifications(user_id,message) VALUES(?,?)",
        (user_id, message)
    )
    conn.commit()
    print("Notification Saved")

# Display Tasks
def show_tasks():
    cursor.execute("""
    SELECT task_id, task_name, status
    FROM tasks
    """)
    for row in cursor.fetchall():
        print(row)

# Example
add_user("admin", "admin123", "Admin")
add_user("kanishka", "12345", "User")

add_task(2, "Account Management", "2026-07-20", "2026-07-21")
update_status(1, "Completed")
send_notification(2, "Your task has been completed.")

show_tasks()

conn.close()
