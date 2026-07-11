import json
from voice import speak

FILE_NAME = "email_history.json"


# ---------------- Load Email History ----------------

'''

@Function Name: load_email_history
@Description  : This function loads email
                history from the
                email_history.json file.
@InputParam   : None
@OutputParam  : Email history
@Author       : Bhoomi Sapke

'''

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

'''

@Function Name: save_email_history
@Description  : This function saves email
                history to the
                email_history.json file.
@InputParam   : records
@OutputParam  : None

'''

def save_email_history(records):
    with open(FILE_NAME, "w") as file:
        json.dump(records, file, indent=4)


# ---------------- Track Email Status ----------------

'''

@Function Name: track_email_status
@Description  : This function checks and
                displays the status of an
                email using its email ID.
@InputParam   : email_id
@OutputParam  : Email status

'''

def track_email_status(email_id):

    records = load_email_history()

    if not records:
        print("No email history found.")
        return
    
    for email in records:

        if email.get("email_id") == email_id:
            print(f"Email Status : {email['status']}")
            return

    print("Email record not found.")


# ---------------- Search by Recipient ----------------

'''

@Function Name: search_by_recipient
@Description  : This function searches
                the email history using
                the recipient email.
@InputParam   : recipient_email
@OutputParam  : Email details

'''

def search_by_recipient(recipient_email):

    records = load_email_history()

    if not records:
        print("No email history found.")
        return
    
    found = False

    for email in records:

        if email.get("recipient_email", "").lower() == recipient_email.lower():

            view_email_details(email["email_id"])
            found = True

    if not found:
        print("No email found.")


# ---------------- Search by Subject ----------------

'''

@Function Name: search_by_subject
@Description  : This function searches
                the email history using
                the email subject.
@InputParam   : subject
@OutputParam  : Email details

'''

def search_by_subject(subject):

    records = load_email_history()

    if not records:
        print("No email history found.")
        return

    found = False

    for email in records:

        if subject.strip().lower() in email.get("subject", "").strip().lower():

            view_email_details(email["email_id"])
            found = True

    if not found:
        print("No email found.")


# ---------------- View Email Details ----------------

'''

@Function Name: view_email_details
@Description  : This function displays
                the details of an email
                using its email ID.
@InputParam   : email_id
@OutputParam  : Email details

'''

def view_email_details(email_id):

    records = load_email_history()

    for email in records:

        if email.get("email_id") == email_id:

            print("--------------------------------------")
            print(f"Email ID        : {email.get('email_id', 'N/A')}")
            print(f"Recipient Email : {email.get('recipient_email', 'N/A')}")
            print(f"Subject         : {email.get('subject', 'N/A')}")
            print(f"Template Name   : {email.get('template_name', 'N/A')}")
            print(f"Message         : {email.get('message', 'N/A')}")
            print(f"Schedule Date   : {email.get('schedule_date', 'N/A')}")
            print(f"Schedule Time   : {email.get('schedule_time', 'N/A')}")
            print(f"Status          : {email.get('status', 'N/A')}")
            print(f"Sent Date       : {email.get('sent_date', 'N/A')}")
            print(f"Sent Time       : {email.get('sent_time', 'N/A')}")
            return

    print("Email record not found.")


# ---------------- Delete Email History ----------------

'''

@Function Name: delete_email_history
@Description  : This function deletes
                all email history from
                the email_history.json
                file.
@InputParam   : None
@OutputParam  : None

'''

def delete_email_history():

    records = load_email_history()

    if not records:
        print("No email history found.")
        speak("No email history found.")
        return

    save_email_history([])

    speak("All email history deleted successfully.")
    print("All email history deleted successfully.")

# ---------------- Tracking ----------------

def tracking_menu():
    
    while True:
        
        print("----- EMAIL TRACKING -----")
        speak("EMAIL TRACKING")
        print("1. Search by Recipient")
        print("2. Search by Subject")
        print("3. View Email Details")
        print("4. Reset Email History")
        print("5. Back")

        ch = input("Enter Choice: ")

        if ch == "1":
            recipient = input("Enter Recipient Email: ")
            search_by_recipient(recipient)

        elif ch == "2":
            subject = input("Enter Subject: ").strip()
            search_by_subject(subject)

        elif ch == "3":
            email_id = int(input("Enter Email ID: "))
            view_email_details(email_id)

        elif ch == "4":
            delete_email_history()

        elif ch == "5":
            break

        else:
            print("Invalid Choice!")

