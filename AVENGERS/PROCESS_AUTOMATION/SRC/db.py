import sqlite3

DB_NAME = "process_automation.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ---------------- USERS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('Admin','User')) NOT NULL
    )
    """)

    # ---------------- TASKS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_name TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        assigned_date TEXT,
        due_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    # ---------------- NOTIFICATIONS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    # ---------------- PROCESSES ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processes (
        process_id INTEGER PRIMARY KEY AUTOINCREMENT,
        process_name TEXT NOT NULL,
        process_details TEXT,
        status TEXT DEFAULT 'Not Executed',
        created_date TEXT,
        created_time TEXT
    )
    """)

    # ---------------- WORKFLOW STEPS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflow_steps (
        step_id INTEGER PRIMARY KEY AUTOINCREMENT,
        process_id INTEGER,
        step_name TEXT,
        FOREIGN KEY(process_id) REFERENCES processes(process_id)
    )
    """)

    # ---------------- FILE LOG ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        action TEXT,
        content TEXT,
        time TEXT
    )
    """)

    # ---------------- TASK LOG ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        status TEXT,
        execution_time TEXT
    )
    """)

    # ---------------- SCHEDULE LOG ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        schedule_time TEXT,
        last_run TEXT
    )
    """)

    # ---------------- SYSTEM LOGS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        task TEXT,
        status TEXT,
        error TEXT
    )
    """)

    conn.commit()
    return conn, cursor


def initialize_database():
    conn, cursor = get_connection()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print("Database created successfully.")