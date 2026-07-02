import csv
import os

from email.message import EmailMessage

from utils import read_csv_recipients, send_with_retry, add_attachments
from compose_email import create_email
from attachments import attachment_menu


def process_csv_emails(provider,
                       provider_config,
                       sender_email,
                       sender_password,
                       msg,
                       subject,
                       body,
                       attachments):

    while True:

        csv_file = input("\nEnter CSV File Name : ").strip()

        if not csv_file:
            print("CSV file name cannot be empty.")
            continue

        if not os.path.exists(csv_file):
            print("CSV file not found.")
            continue

        break

    valid_recipients, duplicate_emails = read_csv_recipients(csv_file)

    if valid_recipients is None:
        return

    if not valid_recipients:
        print("\nNo Valid Email Addresses Found.")
        return

    print("\nSummary")
    print("---------------------------")
    print(f"Valid Emails      : {len(valid_recipients)}")
    print(f"Duplicates Removed: {len(duplicate_emails)}")
    print("---------------------------")

    # If compose_email() was not called from main
    if msg is None:

        msg, subject, body = create_email()

        if msg is None:
            return

    # If attachments were not selected from main
    if attachments is None:

        attachments = attachment_menu()

    print("\nStarting Email Sending...\n")
    success_count = 0
    failed_count = 0

    for receiver in valid_recipients:

        receiver_email = receiver["email"]
        name = receiver["name"]

        email_msg = EmailMessage()

        email_msg["From"] = sender_email
        email_msg["To"] = receiver_email
        email_msg["Subject"] = subject

        personalized_body = body.replace("{name}", name)

        email_msg.set_content(personalized_body)

        if attachments:
            email_msg = add_attachments(email_msg, attachments)

        print(f"\nSending Email To : {receiver_email}")

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
    print("        EMAIL SENDING SUMMARY")
    print("========================================")
    print(f"Total Valid Emails : {len(valid_recipients)}")
    print(f"Successfully Sent  : {success_count}")
    print(f"Failed             : {failed_count}")
    print("========================================")

    if duplicate_emails:

        print("\nDuplicate Emails Removed:")

        for email in sorted(duplicate_emails):
            print(email)

    print("\nEmail Processing Completed Successfully.")
