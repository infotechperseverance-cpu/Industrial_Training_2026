# =============================================================================
# FILE NAME : send_email.py
# PROJECT : EMAIL AUTOMATION SYSTEM
# MODULE NAME : Send Email System
# DESCRIPTION: Sends emails using Gmail SMTP.
# Supports: 1. Receiver management, 2. Attachment sending, 3. Email reports
# DATABASE: email_automation
# =============================================================================

import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage
import mysql.connector
from mysql.connector import Error

from ai_email import AIEmailWriter
from attachment import AttachmentManager


# =============================================================================
# DATABASE CONNECTION
# =============================================================================
def db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="email_automation"
        )
        return connection
    except Error as err:
        print("\nDatabase Connection Error :", err)
        return None


# =============================================================================
# CREATE DATABASE TABLES
# =============================================================================
def create_tables():
    conn = db_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        # EMAIL ACCOUNT TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_accounts
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE,
            app_password VARCHAR(255)
        )
        """)

        # RECEIVER TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS receiver_email
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            receiver_email VARCHAR(255) UNIQUE
        )
        """)

        # EMAIL REPORT TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_reports
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            recipient_email VARCHAR(255),
            subject VARCHAR(255),
            status VARCHAR(50),
            sent_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        print("\nDatabase Tables Ready.")
    except Error as err:
        print("\nTable Creation Error :", err)
    finally:
        cursor.close()
        conn.close()


# =============================================================================
# CLASS NAME : SendEmail
# =============================================================================
class SendEmail:

    def __init__(self):
        create_tables()
        self.connection = db_connection()
        if self.connection is None:
            exit()
        self.cursor = self.connection.cursor()
        self.load_sender()

    def load_sender(self):
        self.cursor.execute("""
            SELECT email, app_password
            FROM email_accounts
            LIMIT 1
        """)
        result = self.cursor.fetchone()
        if result:
            self.email = result[0]
            self.password = result[1]
        else:
            print("\nNo Sender Email Found.")
            print("Please insert Gmail ID and App Password into email_accounts table.")
            self.email = None
            self.password = None

    def add_receiver(self):
        name = input("\nReceiver Name : ").strip()
        email = input("Receiver Email : ").strip()

        self.cursor.execute(
            "SELECT id FROM receiver_email WHERE receiver_email=%s",
            (email,)
        )
        result = self.cursor.fetchone()
        if result:
            return email

        self.cursor.execute(
            "INSERT INTO receiver_email (name, receiver_email) VALUES (%s, %s)",
            (name, email)
        )
        self.connection.commit()
        print("\nReceiver Added Successfully.")
        return email

    def save_report(self, receiver, subject, status):
        query = """
        INSERT INTO email_reports (recipient_email, subject, status)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (receiver, subject, status))
        self.connection.commit()

    def send_mail(self):
        if self.email is None or self.password is None:
            print("\nSender Gmail Account Not Configured.")
            return

        receiver_email = self.add_receiver()

        print("\n======================================")
        print("        EMAIL GENERATION")
        print("======================================")
        print("1. Manual Email")
        print("2. AI Generated Email")
        print("======================================")

        choice = input("Enter Choice : ").strip()

        if choice == "1":
            subject = input("\nEnter Subject : ").strip()
            print("\nEnter Email Message")
            print("Press ENTER twice to finish.\n")

            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            message = "\n".join(lines)

        elif choice == "2":
            topic = input("\nEnter Email Topic : ").strip()
            tone = input("Enter Email Tone : ").strip()
            details = input("Enter Additional Details : ").strip()

            ai = AIEmailWriter()
            subject, message = ai.generate_email(topic, tone, details)

            if subject == "Error":
                print(message)
                return

            print("\n===================================")
            print("AI EMAIL GENERATED")
            print("===================================")
            print("\nSubject :")
            print(subject)
            print("\nBody :")
            print(message)

        else:
            print("\nInvalid Choice.")
            return

        email = EmailMessage()
        email["From"] = self.email
        email["To"] = receiver_email
        email["Subject"] = subject
        email.set_content(message)

        file_path = input("\nEnter Attachment Path (Press Enter to Skip) : ").strip()
        if file_path != "":
            try:
                manager = AttachmentManager()
                manager.add_attachment(email, file_path)
                print("Attachment Added Successfully.")
            except Exception as e:
                print("Attachment Error :", e)
                return

        try:
            print("\nConnecting To Gmail Server...")
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
            server.login(self.email, self.password)
            print("Logged Into Gmail Successfully.")

            server.send_message(email)
            server.quit()

            print("\n======================================")
            print(" Email Sent Successfully")
            print("======================================")
            print("Receiver :", receiver_email)
            print("Subject  :", subject)
            print("Time     :", datetime.now())

            self.save_report(receiver_email, subject, "Success")

        except Exception as e:
            print("\nEmail Sending Failed.")
            print("Reason :", e)
            self.save_report(receiver_email, subject, "Failed")

    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
        except:
            pass

        try:
            if self.connection:
                self.connection.close()
        except:
            pass

        print("\nDatabase Connection Closed.")


# =============================================================================
# MAIN PROGRAM
# =============================================================================
if __name__ == "__main__":
    print("\n========================================")
    print("        SEND EMAIL MODULE")
    print("========================================")

    try:
        obj = SendEmail()
        obj.send_mail()
        obj.close_connection()
    except KeyboardInterrupt:
        print("\n\nProgram Interrupted By User.")
    except Exception as e:
        print("\nUnexpected Error :", e)
