import json

FILE_NAME = "email_history.json"


# ---------------- Load Email History ----------------

def load_email_history():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        with open(FILE_NAME, "w") as file:
            json.dump([], file, indent=4)
        return []

    except json.JSONDecodeError:
        return []


# ---------------- Save Email History ----------------

def save_email_history(records):
    with open(FILE_NAME, "w") as file:
        json.dump(records, file, indent=4)


# ---------------- Track Email Status ----------------

def track_email_status(email_id):

    records = load_email_history()

    if not records:
        print("No email history found.")
        return
    
    for email in records:

        if email["email_id"] == email_id:
            print(f"Email Status : {email['status']}")
            return

    print("Email record not found.")


# ---------------- Search by Recipient ----------------

def search_by_recipient(recipient_email):

    records = load_email_history()

    if not records:
        print("No email history found.")
        return
    
    found = False

    for email in records:

        if email["recipient_email"].lower() == recipient_email.lower():

            view_email_details(email["email_id"])
            found = True

    if not found:
        print("No email found.")


# ---------------- Search by Subject ----------------

def search_by_subject(subject):

    records = load_email_history()

    if not records:
        print("No email history found.")
        return

    found = False

    for email in records:

        if subject.lower() in email["subject"].lower():

            view_email_details(email["email_id"])
            found = True

    if not found:
        print("No email found.")


# ---------------- View Email Details ----------------

def view_email_details(email_id):

    records = load_email_history()

    for email in records:

        if email["email_id"] == email_id:

            print("--------------------------------------")
            print(f"Email ID        : {email['email_id']}")
            print(f"Recipient Email : {email['recipient_email']}")
            print(f"Subject         : {email['subject']}")
            print(f"Template Name   : {email['template_name']}")
            print(f"Message         : {email['message']}")
            print(f"Schedule Date   : {email['schedule_date']}")
            print(f"Schedule Time   : {email['schedule_time']}")
            print(f"Status          : {email['status']}")
            print(f"Sent Date       : {email['sent_date']}")
            print(f"Sent Time       : {email['sent_time']}")
            return

    print("Email record not found.")


# ---------------- Delete Email History ----------------

def delete_email_history(email_id):

    records = load_email_history()

    for email in records:

        if email["email_id"] == email_id:

            records.remove(email)

            save_email_history(records)

            print("Email history deleted successfully.")
            return

    print("Email record not found.")

# ---------------- Tracking ----------------

def tracking_menu():
    while True:
        print("\n----- EMAIL TRACKING -----")
        print("1. Search by Recipient")
        print("2. Search by Subject")
        print("3. View Email Details")
        print("4. Back")

        ch = input("Enter Choice: ")

        if ch == "1":
            recipient = input("Enter Recipient Email: ")
            search_by_recipient(recipient)

        elif ch == "2":
            subject = input("Enter Subject: ")
            search_by_subject(subject)

        elif ch == "3":
            email_id = input("Enter Email ID: ")
            view_email_details(email_id)

        elif ch == "4":
            break

        else:
            print("Invalid Choice!")

