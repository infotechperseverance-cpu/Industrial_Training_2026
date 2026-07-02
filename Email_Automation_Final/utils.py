import csv
import os
import re
import time
import smtplib
import socket


from datetime import datetime
from email.message import EmailMessage


# ==========================================================
# EMAIL VALIDATION
# ==========================================================

def is_valid_email(email):

    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    return bool(re.match(pattern, email))


# ==========================================================
# INTERNET CONNECTION CHECK
# ==========================================================

def check_internet():

    try:

        socket.create_connection(("8.8.8.8", 53), timeout=5)

        return True

    except OSError:

        return False


# ==========================================================
# LOG EMAIL STATUS
# ==========================================================

def log_email_status(receiver_email,
                     subject,
                     status,
                     provider):

    file_exists = os.path.exists("logs.csv")

    with open(
            "logs.csv",
            "a",
            newline="",
            encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow(
                [
                    "Receiver",
                    "Subject",
                    "Status",
                    "Provider",
                    "Date",
                    "Time"
                ]
            )

        now = datetime.now()

        writer.writerow(
            [
                receiver_email,
                subject,
                status,
                provider,
                now.strftime("%d-%m-%Y"),
                now.strftime("%H:%M:%S")
            ]
        )


# ==========================================================
# ADD ATTACHMENTS
# ==========================================================

def add_attachments(msg,
                    attachments):

    if not attachments:

        return msg

    for file_path in attachments:

        try:

            with open(file_path, "rb") as file:

                file_data = file.read()

            file_name = os.path.basename(file_path)

            msg.add_attachment(

                file_data,

                maintype="application",

                subtype="octet-stream",

                filename=file_name

            )

        except Exception as e:

            print(f"Attachment Error : {e}")

    return msg


# ==========================================================
# SEND EMAIL WITH RETRY
# ==========================================================

def send_with_retry(msg,
                    sender_email,
                    sender_password,
                    smtp_server,
                    smtp_port,
                    provider,
                    save_callback=None):

    if not check_internet():

        print("\nNo Internet Connection.")

        log_email_status(
            msg["To"],
            msg["Subject"],
            "Internet Failed",
            provider
        )

        return False

    for attempt in range(1, 4):

        try:

            with smtplib.SMTP(
                    smtp_server,
                    smtp_port
            ) as smtp:

                smtp.starttls()

                smtp.login(
                    sender_email,
                    sender_password
                )

                smtp.send_message(msg)
                from email.utils import make_msgid

                if "Message-ID" not in msg:
                    msg["Message-ID"] = make_msgid()

                message_id = msg["Message-ID"]
            print(
                f"Email sent successfully to {msg['To']}"
            )
            try:
                from logging_reply import log_email
                log_email(
                    msg["To"],
                    msg["Subject"],
                    "Sent",
                    "Success",
                    message_id
                )
            except Exception:
                pass

            log_email_status(

                msg["To"],

                msg["Subject"],

                "Success",

                provider

            )

            if save_callback:

                save_callback(
                    msg["To"]
                )

            return True

        except Exception as e:

            print(
                f"\nAttempt {attempt}/3 Failed"
            )

            print(e)

            if attempt < 3:

                print(
                    "Retrying..."
                )

                time.sleep(2)

    print(
        f"Could not send email to {msg['To']}"
    )
    try:
        from logging_reply import log_email
        log_email(
            msg["To"],
            msg["Subject"],
            "Sent",
            "Failed",
            ""
        )
    except Exception:
        pass

    log_email_status(

        msg["To"],

        msg["Subject"],

        "Failed",

        provider

    )

    return False

import csv
import os


def read_csv_recipients(csv_file):

    valid_recipients = []
    duplicate_emails = set()
    unique_emails = set()

    if not os.path.exists(csv_file):
        print("CSV File not found.")
        return None, None

    try:

        with open(csv_file, "r", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("CSV File is empty.")
                return None, None

            if "name" not in reader.fieldnames:
                print("Column 'name' not found.")
                return None, None

            if "email" not in reader.fieldnames:
                print("Column 'email' not found.")
                return None, None

            for row in reader:

                receiver_email = row["email"].strip()
                name = row["name"].strip()

                if not is_valid_email(receiver_email):
                    print(f"Invalid Email : {receiver_email}")
                    continue

                email_lower = receiver_email.lower()

                if email_lower in unique_emails:

                    duplicate_emails.add(email_lower)
                    print(f"Duplicate Removed : {receiver_email}")

                    continue

                unique_emails.add(email_lower)

                valid_recipients.append({
                    "name": name,
                    "email": receiver_email
                })

        return valid_recipients, duplicate_emails

    except PermissionError:

        print("Permission Denied.")
        return None, None

    except csv.Error as e:

        print(f"CSV Error : {e}")
        return None, None

    except Exception as e:

        print(f"Error : {e}")
        return None, None