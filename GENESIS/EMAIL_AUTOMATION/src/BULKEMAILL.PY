import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------- DATABASE CONNECTION ----------------

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pass@123",      #  MySQL password
        database="bulk_email_system"
    )

# ---------------- GET CONTACTS ----------------

def get_contacts():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name,email FROM contacts")
    contacts = cursor.fetchall()

    conn.close()
    return contacts

# ---------------- SAVE REPORT ----------------

def save_report(email, subject, status):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO email_reports(recipient_email,subject,status)
    VALUES(%s,%s,%s)
    """, (email, subject, status))

    conn.commit()
    conn.close()

# ---------------- SEND BULK EMAIL ----------------

def send_bulk_email():

    sender_email = input("Enter Gmail : ")
    app_password = input("Enter App Password : ")

    subject = input("Enter Subject : ")

    print("\nUse {name} where you want the recipient's name.")
    message = input("Enter Message : ")

    contacts = get_contacts()

    if len(contacts) == 0:
        print("No Contacts Found.")
        return

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)

    success = 0
    failed = 0

    print("\n========== Sending Emails ==========\n")

    for name, email in contacts:

        body = message.replace("{name}", name)

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            server.sendmail(sender_email, email, msg.as_string())
            print(f"✓ Email Sent -> {name} ({email})")
            save_report(email, subject, "Success")
            success += 1

        except Exception:
            print(f"✗ Failed -> {name} ({email})")
            save_report(email, subject, "Failed")
            failed += 1

    server.quit()

    print("\n========== SUMMARY ==========")
    print("Total Contacts :", len(contacts))
    print("Emails Sent    :", success)
    print("Failed         :", failed)

# ---------------- MAIN ----------------

send_bulk_email()