import mysql.connector
from mysql.connector import Error
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from plyer import notification

def connect_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="task_scheduler_db"
        )
        if connection.is_connected():
            return connection
    except Error:
        return None

def send_email(receiver_email, subject, message):
    sender_email = "adityagahelwar81@gmail.com"
    sender_password = "enzf ytor vgfz uaud"

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception:
        pass

def show_notification(title, message):
    try:
        notification.notify(title=title, message=message, timeout=10)
    except Exception:
        pass

def check_overdue_tasks(username):
    connection = connect_database()
    if not connection:
        return

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)

        user_query = "SELECT id, email, name FROM users WHERE username = %s"
        cursor.execute(user_query, [username])
        user = cursor.fetchone()

        if not user:
            return

        user_id = user['id']
        user_email = user['email']
        user_name = user['name']

        overdue_query = "SELECT title, deadline FROM tasks WHERE user_id = %s AND status = 'overdue'"
        cursor.execute(overdue_query, [user_id])
        overdue_tasks = cursor.fetchall()

        if overdue_tasks:
            task_list_str = ""
            for task in overdue_tasks:
                task_list_str += f"- {task['title']} (Deadline: {task['deadline']})\n"

            email_subject = "Urgent: Overdue Tasks Alert"
            email_message = f"Hello {user_name},\n\nYou have overdue tasks that require your immediate attention:\n\n{task_list_str}\nRegards,\nTask Scheduler System"

            show_notification("TASK OVERDUE ALERT", f"Hi {user_name}, you have {len(overdue_tasks)} overdue task(s)!")
            send_email(user_email, email_subject, email_message)

    except Exception:
        pass
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    pass