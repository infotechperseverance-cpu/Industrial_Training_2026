import json
import csv
import smtplib
import os
import re
import time
import winsound
from plyer import notification
from email.message import EmailMessage
from datetime import datetime
from email_tracking import load_email_history, save_email_history
from email_management import load_email_records, save_email_records,validate_email,update_email_status
from reports_logs import save_log


# EMAIL_RECORDS_FILE = "email_records.json"
# EMAIL_HISTORY_FILE = "email_history.json"
USER_FILE = "user_data.csv"


# ---------------- SEND EMAIL ----------------

def send_email(sender_email,
               sender_password,
               recipient_email,
               subject,
               message,
               attachment):

    try:
        
       # print("Creating Email Message")
        mail = EmailMessage()

        mail["From"] = sender_email
        mail["To"] = recipient_email
        mail["Subject"] = subject

        mail.set_content(message)

        if attachment != "" and os.path.isfile(attachment):

            with open(attachment, "rb") as file:

                mail.add_attachment(
                    file.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename=os.path.basename(attachment)
                )
        # print("Connecting to SMTP")

        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        # print("Starting TLS")
        smtp.starttls()

        smtp.login(sender_email, sender_password)
        # print("Sending Message")
        smtp.send_message(mail)
        # print("Closing Connection")
        smtp.quit()
        # print("Email Sent Successfully")
        return True

    except Exception as e:

        print("Email Sending Failed")

        print(e)

        return False
    
def process_emails(sender_email, sender_password):

    records = load_email_records()

    if sender_email is None:
        print("Login required.")
        return

    for record in records:

        if record["status"].lower() in ["completed", "sending"]:
            continue

        process_single_email(record, sender_email, sender_password, records)

    save_email_records(records)
    
    

def process_single_email(record, sender_email, sender_password, records):

    if record["status"].lower() in ["completed", "sending"]:
        return

    if not validate_email(record["recipient_email"]):
        record["status"] = "failed"
        save_email_records(records)

        print_email_report(record, "FAILED ❌", "Invalid email address")
        return

    if not check_schedule(record):
        print_email_report(record, "PENDING ⏳", "Scheduled for later delivery")

    record["status"] = "sending"
    save_email_records(records)

    success = send_email(
        sender_email,
        sender_password,
        record["recipient_email"],
        record["subject"],
        record["message"],
        record.get("attachment", "")
    )

    if success:
        record["status"] = "completed"
        save_email_records(records)
        save_to_history(record)
        save_log(record["email_id"], "Email Sent")
        print_email_report(record, "SENT SUCCESSFULLY ✅", "Email delivered and stored in history")
        show_success_notification()

    else:
        record["status"] = "failed"
        save_email_records(records)

        print_email_report(record, "FAILED ❌", "SMTP sending failed")


def check_schedule(record):

    schedule_str = record["schedule_date"] + " " + record["schedule_time"]

    schedule = datetime.strptime(schedule_str, "%Y-%m-%d %I:%M %p")
    now = datetime.now()

    if schedule > now:
        print(f"⏳ Scheduled for later: {schedule}")
        return False   # IMPORTANT: do NOT sleep

    return True

def save_to_history(record):

    history = load_email_history()

    history.append({

        "email_id": record["email_id"],
        "recipient_email": record["recipient_email"],
        "subject": record["subject"],
        "template_name": record["template_name"],
        "message": record["message"],
        "schedule_date": record["schedule_date"],
        "schedule_time": record["schedule_time"],
        "status": "Completed",
        "sent_date": datetime.now().strftime("%Y-%m-%d"),
        "sent_time": datetime.now().strftime("%H:%M:%S")

    })

    save_email_history(history)

def print_email_report(record, status, message):
    print("\n========================================")
    print(" EMAIL AUTOMATION SYSTEM REPORT")
    print("========================================")

    print(f" Email ID      : {record['email_id']}")
    print(f" Recipient     : {record['recipient_email']}")
    print(f" Subject         : {record['subject']}")
    print(f" Status          : {status}")
    print(f" Message         : {message}")
    print("========================================\n")

def show_success_notification():

    notification.notify(
        title="Email Automation",
        message="Email sent successfully!",
        app_name="Email Automation System",
        timeout=5
    )
    winsound.MessageBeep(winsound.MB_ICONASTERISK)

