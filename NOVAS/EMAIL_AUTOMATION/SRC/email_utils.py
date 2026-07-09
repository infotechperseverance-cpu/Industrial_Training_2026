import json
import re
from voice import speak
FILE_NAME = "email_records.json"

# ---------------- Load Email Records ----------------

def load_email_records():
    try:
       # print("Opening:", FILE_NAME)

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

#---------------- Assign Email IDs ----------------

def assign_email_ids():
    records = load_email_records()

    next_id = 1
    updated = False

    for email in records:
        if not email.get("email_id"):
            email["email_id"] = str(next_id)
            updated = True
        next_id += 1

    if updated:
        save_email_records(records)
        speak("Email IDs were generated automatically.")
        print("Email IDs were generated automatically.")
        

#---------------- Fix Duplicate Email IDs ----------------

def fix_duplicate_email_ids():
    records = load_email_records()

    used_ids = set()
    max_id = 0

    # Find the current maximum numeric ID
    for email in records:
        try:
            max_id = max(max_id, int(email.get("email_id", 0)))
        except ValueError:
            pass

    updated = False

    for email in records:
        email_id = str(email.get("email_id", "")).strip()

        if not email_id or email_id in used_ids:
            max_id += 1
            email["email_id"] = str(max_id)
            updated = True

        used_ids.add(email["email_id"])

    if updated:
        save_email_records(records)
        speak("Duplicate or missing Email IDs were fixed automatically.")
        print("Duplicate or missing Email IDs were fixed automatically.")
      
