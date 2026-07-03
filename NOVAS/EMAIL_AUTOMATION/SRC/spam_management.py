import json

FILE_NAME = "email_records.json"

SPAM_KEYWORDS = [
    "sale",
    "offer",
    "discount",
    "free",
    "winner",
    "lottery",
    "cashback",
    "buy now",
    "click here",
    "limited time"
]


# ---------------- Load Email Records ----------------

def load_email_records():

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


# ---------------- Save Email Records ----------------

def save_email_records(records):

    with open(FILE_NAME, "w") as file:
        json.dump(records, file, indent=4)


# ---------------- Detect Spam ----------------

def detect_spam(email):

    text = (email["subject"] + " " + email["message"]).lower()

    for keyword in SPAM_KEYWORDS:

        if keyword in text:
            return True

    return False


# ---------------- Mark Email as Spam ----------------

def mark_as_spam():

    records = load_email_records()

    found = False

    for email in records:

        if detect_spam(email):

            email["status"] = "Spam"
            found = True

    if found:
        save_email_records(records)
        print("Spam emails marked successfully.")
    else:
        print("No spam emails found.")


# ---------------- View Spam List ----------------

def view_spam_list():

    records = load_email_records()

    found = False

    for email in records:

        if email["status"] == "Spam":

            print("-" * 40)
            print("Email ID :", email["email_id"])
            print("Recipient:", email["recipient_email"])
            print("Subject  :", email["subject"])
            print("Status   :", email["status"])

            found = True

    if not found:
        print("No spam emails found.")


# ---------------- Delete Spam Emails ----------------

def delete_spam_emails():

    records = load_email_records()

    new_records = []

    for email in records:

        if email["status"] != "Spam":
            new_records.append(email)

    save_email_records(new_records)

    print("All spam emails deleted successfully.")

# ---------------- Spam ----------------

def spam_menu():
    while True:
        print("\n----- SPAM MANAGEMENT -----")
        print("1. Mark as Spam")
        print("2. View Spam List")
        print("3. Delete Spam Email")
        print("4. Back")

        ch = input("Enter Choice: ")

        if ch == "1":
            mark_as_spam()

        elif ch == "2":
            view_spam_list()

        elif ch == "3":
            delete_spam_emails()

        elif ch == "4":
            break

        else:
            print("Invalid Choice!")