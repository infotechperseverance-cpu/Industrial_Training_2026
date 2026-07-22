import mysql.connector
from datetime import datetime

# ---------------- DATABASE CONNECTION -----------------------

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pass@123",
        database="bulk_email_system"
    )

# ---------------- CREATE TABLE -------------------------------

def create_table():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_reminders(
        id INT AUTO_INCREMENT PRIMARY KEY,
        recipient_email VARCHAR(100),
        subject VARCHAR(255),
        message TEXT,
        reminder_date DATETIME,
        status VARCHAR(20) DEFAULT 'Pending'
    )
    """)

    conn.commit()
    conn.close()

# ---------------- ADD REMINDER ------------------------------

def add_reminder():
    conn = db_connection()
    cursor = conn.cursor()

    email = input("Recipient Email : ")
    subject = input("Subject : ")
    message = input("Message : ")
    date = input("Reminder Date (YYYY-MM-DD HH:MM:SS): ")

    sql = """
    INSERT INTO email_reminders
    (recipient_email, subject, message, reminder_date)
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(sql, (email, subject, message, date))
    conn.commit()

    print("\nReminder Saved Successfully.")

    conn.close()

# ---------------- VIEW REMINDERS ----------------

def view_reminders():

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM email_reminders")

    data = cursor.fetchall()

    print("\n========== EMAIL REMINDERS ==========")

    for row in data:
        print(row)

    conn.close()

# ---------------- MAIN ----------------

create_table()

while True:

    print("\n===== EMAIL REMINDER SYSTEM =====")
    print("1. Add Reminder")
    print("2. View Reminder")
    print("3. Exit")

    choice = input("Enter Choice : ")

    if choice == "1":
        add_reminder()

    elif choice == "2":
        view_reminders()

    elif choice == "3":
        print("Thank You")
        break

    else:
        print("Invalid Choice")