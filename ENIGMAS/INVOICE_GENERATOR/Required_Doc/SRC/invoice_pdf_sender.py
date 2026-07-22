import smtplib
from email.message import EmailMessage
import os
import re

'''
Function Name : send_invoice
Purpose       : Read customer's email and send invoice.pdf to that email.
Input         : email, file_path
Output        : True if email sent successfully, otherwise False.
author        : harsh patil
'''

def send_invoice(email, file_path):
    try:
        # Validate inputs
        if not email or not file_path:
            print("Email and PDF file path are required.")a
            return False

        # Validate email format
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(pattern, email):
            print("Invalid email address.")
            return False

        # Check file exists
        if not os.path.isfile(file_path):
            print("PDF file not found.")
            return False

        # Check PDF extension
        if os.path.splitext(file_path)[1].lower() != ".pdf":
            print("Selected file is not a PDF.")
            return False

        choice = input("Do you want to send Email? (Y/N): ")

        if choice.lower() != "y":
            print("Email cancelled.")
            return False

        # Sender details
        sender_email = "patilharshwardhan218@gmail.com"

        # Replace with your Gmail App Password
        app_password = ""

        # Create Email
        msg = EmailMessage()

        msg["Subject"] = "Invoice from Enigmas Supermarket"
        msg["From"] = sender_email
        msg["To"] = email

        msg.set_content(
"""Dear Customer,

Thank you for shopping with us.

Your invoice is attached with this email.

Thank You,
Enigmas Supermarket
"""
        )

        # Attach PDF
        with open(file_path, "rb") as file:
            msg.add_attachment(
                file.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(file_path)
            )

        print("Connecting to Gmail server...")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            print("Logging in...")
            server.login(sender_email, app_password)

            print("Sending email...")
            server.send_message(msg)

        print("\nEmail Sent Successfully.")
        return True

    except smtplib.SMTPAuthenticationError:
        print("Authentication failed.")
        print("Please use a valid Gmail App Password.")
        return False

    except smtplib.SMTPRecipientsRefused:
        print("Recipient email address was refused.")
        return False

    except FileNotFoundError:
        print("PDF file not found.")
        return False

    except KeyboardInterrupt:
        print("\nKeyboard Interrupt.")
        return False

    except Exception as e:
        print("\nError:", e)
        return False


