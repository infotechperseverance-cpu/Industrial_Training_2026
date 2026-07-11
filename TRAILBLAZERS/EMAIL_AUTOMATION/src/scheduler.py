import os
import time

from datetime import datetime
from email.message import EmailMessage

from utils import read_csv_recipients, add_attachments, send_with_retry


def schedule_email(provider,
                   provider_config,
                   sender_email,
                   sender_password,
                   subject,
                   body,
                   attachments):

    while True:

        csv_file = input("\nEnter CSV File Name : ").strip()

        if not csv_file:
            print("CSV File Name cannot be empty.")
            continue

        if not os.path.exists(csv_file):
            print("CSV File not found.")
            continue

        break

    valid_recipients, duplicate_emails = read_csv_recipients(csv_file)

    if valid_recipients is None:
        return

    if not valid_recipients:
        print("No Valid Email Addresses Found.")
        return

    while True:

        schedule_date = input("\nEnter Schedule Date (DD-MM-YYYY) : ").strip()

        try:
            datetime.strptime(schedule_date, "%d-%m-%Y")
            break

        except ValueError:
            print("Invalid Date Format.")

    while True:

        schedule_time = input("Enter Schedule Time (HH:MM) : ").strip()

        try:
            datetime.strptime(schedule_time, "%H:%M")
            break

        except ValueError:
            print("Invalid Time Format.")

    schedule_datetime = datetime.strptime(
        f"{schedule_date} {schedule_time}",
        "%d-%m-%Y %H:%M"
    )

    current_datetime = datetime.now()

    if schedule_datetime <= current_datetime:
        print("Scheduled Date and Time must be in the future.")
        return

    waiting_seconds = (schedule_datetime - current_datetime).total_seconds()

    print("\n========================================")
    print("         EMAIL SCHEDULED")
    print("========================================")
    print(f"Date       : {schedule_date}")
    print(f"Time       : {schedule_time}")
    print(f"Recipients : {len(valid_recipients)}")
    print("Waiting for scheduled time...")
    time.sleep(waiting_seconds)

    print("\nScheduled Time Reached.")
    print("Sending Emails...\n")

    success_count = 0
    failed_count = 0

    for receiver in valid_recipients:

        receiver_email = receiver["email"]
        receiver_name = receiver["name"]

        email_msg = EmailMessage()

        email_msg["From"] = sender_email
        email_msg["To"] = receiver_email
        email_msg["Subject"] = subject

        personalized_body = body
        personalized_body = personalized_body.replace("{name}", receiver_name)
        personalized_body = personalized_body.replace(
            "{date}",
            datetime.now().strftime("%d-%m-%Y")
        )

        email_msg.set_content(personalized_body)

        if attachments:
            email_msg = add_attachments(email_msg, attachments)

        print(f"Sending Email To : {receiver_email}")

        sent = send_with_retry(
            email_msg,
            sender_email,
            sender_password,
            provider_config["smtp_server"],
            provider_config["smtp_port"],
            provider
        )

        if sent:
            success_count += 1
        else:
            failed_count += 1

    print("\n========================================")
    print("     SCHEDULED EMAIL SUMMARY")
    print("========================================")
    print(f"Total Valid Emails : {len(valid_recipients)}")
    print(f"Successfully Sent  : {success_count}")
    print(f"Failed             : {failed_count}")

    if duplicate_emails:

        print("\nDuplicate Emails Removed:")

        for email in sorted(duplicate_emails):
            print(email)

    print("\nScheduled Email Process Completed Successfully.")