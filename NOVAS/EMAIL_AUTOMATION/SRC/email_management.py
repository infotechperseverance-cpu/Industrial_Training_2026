import json
import re
from template import view_template, load_json, save_json,create_template, delete_template, update_template
from voice import speak

FILE_NAME = "email_records.json"


# ---------------- Load Email Records ----------------

def load_email_records():
    try:
        print("Opening:", FILE_NAME)

        with open(FILE_NAME, "r") as file:
            records = json.load(file)

       # print("Records Loaded:", records)

        return records

    except FileNotFoundError:
        print("File Not Found!")
        return []

    except json.JSONDecodeError:
        print("Invalid JSON!")
        return []


# ---------------- Save Email Records ----------------

def save_email_records(records):
    with open(FILE_NAME, "w") as file:
        json.dump(records, file, indent=4)


# ---------------- Validate Email ----------------

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# ---------------- View Email Records ----------------

def view_email_records():

    records = load_email_records()

    if not records:
        print("No email records found.")
        return

    for email in records:
        print("-" * 50)
        print(f"Email ID        : {email['email_id']}")
        print(f"Recipient Email : {email['recipient_email']}")
        print(f"Subject         : {email['subject']}")
        print(f"Template Name   : {email['template_name']}")
        print(f"Message         : {email['message']}")
        print(f"Schedule Date   : {email['schedule_date']}")
        print(f"Schedule Time   : {email['schedule_time']}")
        print(f"Status          : {email['status']}")


# ---------------- Update Email Record ----------------
def update_email_status(email_id, status):

    records = load_email_records()

    for email in records:
        if email["email_id"] == email_id:
            email["status"] = status
            break

    save_email_records(records)

# ---------------- Delete Email Record ----------------

def delete_email_record(email_id):

    records = load_email_records()

    for email in records:

        if email["email_id"] == email_id:

            records.remove(email)

            save_email_records(records)

            print("Email record deleted successfully.")
            return

    print("Email ID not found.")


# ---------------- Email Management ----------------

def email_management_menu():
    speak("----- EMAIL MANAGEMENT -----")
    while True:
        
        print("1. View Email Records")
        print("2. Update Email Status")
        print("3. Delete Email Record")
        print("4. Back")

        ch = input("Enter Choice: ")

        if ch == "1":
            view_email_records()            

        elif ch == "2":
            email_id = input("Enter Email ID: ")
            status = input("Enter new status: ")
            update_email_status(email_id, status)

        elif ch == "3":
            email_id = input("Enter Email ID: ")
            delete_email_record(email_id)

        elif ch == "4":
            break

        else:
            print("Invalid Choice!")
