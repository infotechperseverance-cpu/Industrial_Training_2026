import smtplib
import mysql.connector
from email.message import EmailMessage
from datetime import datetime
import time


class FollowUpEmail:

    def __init__(self):

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pass@123",
            database="email_db"
        )

        self.cursor = self.connection.cursor()

        # Fetch sender email and password
        self.cursor.execute(
            "SELECT email, password FROM email_id WHERE id=1"
        )

        result = self.cursor.fetchone()

        self.email = result[0]
        self.password = result[1]

    # Display all receivers
    def display_receivers(self):

        self.cursor.execute(
            "SELECT id, name, receiver_email FROM receiver_email"
        )

        data = self.cursor.fetchall()

        print("\n========== Receiver List ==========")

        for row in data:
            print(f"ID    : {row[0]}")
            print(f"Name  : {row[1]}")
            print(f"Email : {row[2]}")
            print("-----------------------------------")

    # Get receiver email using ID
    def get_receiver_email(self, receiver_id):

        self.cursor.execute(
            "SELECT receiver_email FROM receiver_email WHERE id=%s",
            (receiver_id,)
        )

        result = self.cursor.fetchone()

        if result:
            return result[0]

        return None

    # Send follow-up email
    def send_followup(self, receiver_email, subject, message, delay_seconds):

        print(f"\nFollow-up email will be sent after {delay_seconds} seconds...")
        time.sleep(delay_seconds)

        email = EmailMessage()

        email["From"] = self.email
        email["To"] = receiver_email
        email["Subject"] = "Follow-up: " + subject
        email.set_content(message)

        try:

            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:

                smtp.starttls()

                smtp.login(self.email, self.password)

                smtp.send_message(email)

            print("Follow-up Email Sent Successfully.")
            print("Sent Time :", datetime.now())

        except Exception as e:

            print("Error :", e)

    def close_connection(self):

        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":

    followup = FollowUpEmail()

    followup.display_receivers()

    receiver_id = int(input("Enter Receiver ID : "))

    receiver = followup.get_receiver_email(receiver_id)

    if receiver is None:
        print("Invalid Receiver ID")
        exit()

    subject = input("Enter Subject : ")
    message = input("Enter Follow-up Message : ")

    delay = int(input("Enter Delay in Seconds : "))

    followup.send_followup(
        receiver,
        subject,
        message,
        delay
    )

    followup.close_connection()