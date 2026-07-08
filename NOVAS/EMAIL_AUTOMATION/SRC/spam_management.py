import json
from voice import speak

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

def auto_detect_spam(records):

    for email in records:

        if detect_spam(email):
            email["status"] = "spam"

    return records

# ---------------- Load Email Records ----------------

def load_email_records():

    try:
        with open(FILE_NAME, "r") as file:
            records = json.load(file)

        records = auto_detect_spam(records)
        save_email_records(records)

        return records

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


