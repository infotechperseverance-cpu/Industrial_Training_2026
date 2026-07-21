import smtplib
import mysql.connector
from email.message import EmailMessage
from attachment import AttachmentManager
from datetime import date

class SendEmail:

    def __init__(self):

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="email_db"
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute(
            "SELECT email,password FROM email_id WHERE id=1"
        )

        result = self.cursor.fetchone()

        self.email = result[0]
        self.password = result[1]

    def display_receivers(self):

        self.cursor.execute(
            "SELECT id,name,receiver_email FROM receiver_email"
        )

        data = self.cursor.fetchall()

        print("\nReceiver List")

      
        print("-" * 45)
        print("ID\tName\t\tEmail")
        print("-" * 45)

        for row in data:
         print(f"{row[0]}\t{row[1]}\t\t{row[2]}")
    def get_receiver_email(self, receiver_id):

        self.cursor.execute(
            "SELECT receiver_email FROM receiver_email WHERE id=%s",
            (receiver_id,)
        )

        result = self.cursor.fetchone()

        if result:
            return result[0]

        return None

    def send_mail(self):

        self.display_receivers()

        receiver_id = int(input("Enter Receiver ID : "))

        receiver_email = self.get_receiver_email(receiver_id)

        if receiver_email is None:
            print("Invalid Receiver ID")
            return

        subject = input("Enter Subject : ")
        message = input("Enter Message : ")

        email = EmailMessage()

        email["From"] = self.email
        email["To"] = receiver_email
        email["Subject"] = subject
        email.set_content(message)

        # Call Attachment Module
        attachment = input("Enter Attachment Path (Press Enter to Skip): ")

        manager = AttachmentManager()
        manager.add_attachment(email, attachment)

        try:

            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:

                smtp.starttls()

                smtp.login(self.email,self.password)

                smtp.send_message(email)

            print("Email Sent Successfully.")
            query = """
            INSERT INTO sent_email
            (receiver_email, subject, message, sent_date,replied, followup_sent,followup_status)
            VALUES (%s, %s, %s, %s, %s,%s,%s)
            """

            values = (
                         receiver_email,
                         subject,
                         message,
                         date.today(),
                         "No",
                         "No",
                         "pending"
                      )

            self.cursor.execute(query, values)
            self.connection.commit()

            print("Email details saved successfully.")
        except Exception as e:

            print("Error :",e)

    def close_connection(self):

        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":

    obj = SendEmail()

    obj.send_mail()

    obj.close_connection()