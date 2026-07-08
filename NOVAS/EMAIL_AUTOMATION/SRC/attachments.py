import os
from email_utils import load_email_records, save_email_records


# ---------------- View Attachments ----------------

def view_attachments():

    records = load_email_records()

    if not records:
        print("No email records found.")
        return

    for email in records:

        print("-" * 50)
        print(f"Email ID  : {email['email_id']}")
        print(f"Recipient : {email['recipient_email']}")
        print(f"Subject   : {email['subject']}")

        attachments = email.get("attachments", [])

        if attachments:
            print("Attachments:")
            for i, file in enumerate(attachments, start=1):
                print(f"{i}. {file}")
        else:
            print("Attachments : None")


# ---------------- Verify Attachments ----------------

def verify_attachments():

    records = load_email_records()

    if not records:
        print("No email records found.")
        return

    for email in records:

        print("-" * 50)
        print(f"Email ID : {email['email_id']}")

        attachments = email.get("attachments", [])

        if not attachments:
            print("No Attachments")
            continue

        for file in attachments:

            if os.path.exists(file):
                print(f"✔ {file}")
            else:
                print(f"✘ {file} (File Not Found)")


# ---------------- Remove Missing Attachments ----------------

def remove_missing_attachments():

    records = load_email_records()

    updated = False

    for email in records:

        attachments = email.get("attachments", [])

        valid_files = []

        for file in attachments:

            if os.path.exists(file):
                valid_files.append(file)
            else:
                print(f"Removed: {file}")

        if len(valid_files) != len(attachments):
            email["attachments"] = valid_files
            updated = True

    if updated:
        save_email_records(records)
        print("\nMissing attachments removed successfully.")
    else:
        print("\nNo missing attachments found.")


# ---------------- Attachment Menu ----------------

def attachment_menu():

    while True:

        print("\n===== Attachment Management =====")
        print("1. View Attachments")
        print("2. Verify Attachments")
        print("3. Remove Missing Attachments")
        print("4. Back")

        ch = input("Enter Choice: ")

        if ch == "1":
            view_attachments()

        elif ch == "2":
            verify_attachments()

        elif ch == "3":
            remove_missing_attachments()

        elif ch == "4":
            break

        else:
            print("Invalid Choice!")