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

'''
@Function Name: detect_spam
@Description  : This function checks the subject and 
                message for spam keywords. 
@InputParam   : email(email received)
@OutputParam  : Spam status
@Author       : Bhoomi Patil

'''

def detect_spam(email):

    text = (email["subject"] + " " + email["message"]).lower()

    for keyword in SPAM_KEYWORDS:

        if keyword in text:
            return True

    return False

'''
@Function Name: auto_detect_spam
@Description  : This function defect_sapam it returns
                True and marks the email as spam..
@InputParam   : records(email_records,json file)
@OutputParam  : Spam status

'''

def auto_detect_spam(records):

    for email in records:

        if detect_spam(email):
            email["status"] = "spam"

    return records

# ---------------- Load Email Records ----------------

'''

@Function Name: load_email_records
@Description  : This function loads email
                records from the JSON file,
                checks for spam emails, and
                returns the updated records.
@InputParam   : None
@OutputParam  : Email records

'''

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

'''
s
@Function Name: save_email_records
@Description  : This function saves the
                email records to the JSON
                file.
@InputParam   : records
@OutputParam  : None

'''

def save_email_records(records):

    with open(FILE_NAME, "w") as file:
        json.dump(records, file, indent=4)





