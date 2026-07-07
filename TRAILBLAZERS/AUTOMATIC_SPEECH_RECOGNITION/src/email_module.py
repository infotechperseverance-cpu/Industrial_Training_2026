"""
=========================================
Email Sending Module
Purpose:
Send emails using voice or text commands.
=========================================
"""
import json
import socket
import smtplib
from email.message import EmailMessage
import mimetypes
import re
import os
import csv
from datetime import datetime

from speech_recognition_module import listen
from voice_engine import speak
from commandHistory import save_command


# -------- Email Validation --------
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# -------- Internet Validation --------
def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except Exception:
        return False

# -------- Load Contacts --------
def load_contacts():

    try:
        with open("contacts.json", "r") as file:

            contact_list = json.load(file)

            contacts = {}

            for contact in contact_list:
                contacts[contact["name"].lower()] = contact["email"]

            return contacts

    except Exception as e:
        print(e)
        speak("Unable to load contacts.")
        return {}


contacts = load_contacts()


# -------- Send Email --------
def send_email(receiver, subject, message, attachment_path=None):

    sender = input("Enter sender email: ")
    password = input("Enter app password: ")

    if not is_valid_email(sender):
        speak("Invalid sender email.")

        return False

    if password.strip() == "":
        speak("Password cannot be empty.")

        return False

    if not check_internet():
        speak("Internet connection is unavailable. Please check your network.")

        return False

    if not is_valid_email(receiver):
        speak("Invalid email address")

        return False

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(message)

    # ---------- Attachment ----------
    allowed_extensions = (
        ".pdf",
        ".doc", ".docx",
        ".xls", ".xlsx",
        ".ppt", ".pptx",
        ".jpg", ".jpeg", ".png", ".gif", ".bmp"
    )

    if attachment_path:

        if not attachment_path.lower().endswith(allowed_extensions):
            speak("Only PDF, Word, Excel, PowerPoint and Image files are allowed.")

            return False

        if not os.path.exists(attachment_path):
            speak("Attachment file not found.")

            return False

        mime_type, _ = mimetypes.guess_type(attachment_path)

        if mime_type is None:
            mime_type = "application/octet-stream"

        maintype, subtype = mime_type.split("/", 1)

        with open(attachment_path, "rb") as file:

            msg.add_attachment(
                file.read(),
                maintype=maintype,
                subtype=subtype,
                filename=os.path.basename(attachment_path)
            )


    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender, password)

        server.send_message(msg)

        server.quit()

        save_email_history(receiver, subject, message, attachment_path)

        speak("Email sent successfully.")



        return True

    except Exception as e:

        print(e)

        speak("Failed to send email.")



        return False


# -------- Email History --------
def save_email_history(receiver, subject, message, attachment):

    file_name = "sent_emails.csv"

    file_exists = os.path.isfile(file_name)

    with open(file_name, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date & Time",
                "Receiver",
                "Subject",
                "Message",
                "Attachment"
            ])

        writer.writerow([
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            receiver,
            subject,
            message,
            attachment if attachment else "No Attachment"
        ])


# -------- Process Email Command --------
def process_email():

    speak("How do you want to enter the recipient?")
    print("\n1. Voice")
    print("2. Text")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        speak("Whom do you want to send the email to?")
        import assistant_state
        assistant_state.assistant_busy = True
        name = listen()
        assistant_state.assistant_busy = False


    elif choice == "2":
        name = input("Enter Contact Name: ").strip().lower()

    else:
        speak("Invalid choice.")
        return False

    if not name:
        speak("Invalid contact.")
        return False

    if name not in contacts:
        speak("Contact not found.")
        return False

    receiver = contacts[name]

    print("\nSubject Input")
    print("1. Voice")
    print("2. Text")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        speak("Speak the subject.")
        import assistant_state
        assistant_state.assistant_busy = True
        subject = listen()
        assistant_state.assistant_busy = False


    elif choice == "2":
        subject = input("Enter Subject: ").strip()

    else:
        speak("Invalid choice.")
        return False

    if subject is None or subject.strip() == "":
        speak("Subject cannot be empty.")
        return False

    print("\nMessage Input")
    print("1. Voice")
    print("2. Text")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        speak("Speak the message.")
        import assistant_state
        assistant_state.assistant_busy = True
        message = listen()
        assistant_state.assistant_busy = False


    elif choice == "2":
        message = input("Enter Message: ").strip()

    else:
        speak("Invalid choice.")
        return False

    if message is None or message.strip() == "":
        speak("Message cannot be empty.")
        return False

    # ---------- Attachment ----------
    attachment = None

    print("\nDo you want to attach a file?")
    choice = input("Enter (yes/no): ").strip().lower()

    if choice == "yes":

        attachment = input(
            "Enter complete file path (PDF, Word, Excel or Image): "
        ).strip()

    elif choice != "no":

        speak("Invalid choice.")
        return False

    # ---------- Final Confirmation ----------
    print("\nDo you want to send the email?")
    confirmation = input("Enter (yes/no): ").strip().lower()

    if confirmation == "yes":

        return send_email(
            receiver,
            subject,
            message,
            attachment
        )

    elif confirmation == "no":

        speak("Email sending cancelled.")
        return False

    else:

        speak("Invalid choice.")
        return False

