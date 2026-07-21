import json
import os

FILE_NAME = "drafts.json"

# Load Drafts
def load_drafts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# Save Drafts
def save_drafts(drafts):
    with open(FILE_NAME, "w") as file:
        json.dump(drafts, file, indent=4)

# Save Draft
def save_draft():
    subject = input("Enter Subject: ")
    recipient = input("Enter Recipient Email: ")
    message = input("Enter Message: ")

    drafts = load_drafts()

    draft = {
        "subject": subject,
        "recipient": recipient,
        "message": message,
        "status": "Draft"
    }

    drafts.append(draft)
    save_drafts(drafts)
    print("Draft Saved Successfully.")

# View Drafts
def view_drafts():
    drafts = load_drafts()

    if not drafts:
        print("No Drafts Found.")
        return

    print("\n----- Draft List -----")
    for i, draft in enumerate(drafts, start=1):
        print(f"\nDraft {i}")
        print("Subject :", draft["subject"])
        print("Recipient :", draft["recipient"])
        print("Message :", draft["message"])
        print("Status :", draft["status"])

# Edit Draft
def edit_draft():
    drafts = load_drafts()

    if not drafts:
        print("No Drafts Available.")
        return

    view_drafts()
    index = int(input("\nEnter Draft Number to Edit: ")) - 1

    if 0 <= index < len(drafts):
        drafts[index]["subject"] = input("New Subject: ")
        drafts[index]["recipient"] = input("New Recipient: ")
        drafts[index]["message"] = input("New Message: ")

        save_drafts(drafts)
        print("Draft Updated Successfully.")
    else:
        print("Invalid Draft Number.")

# Delete Draft
def delete_draft():
    drafts = load_drafts()

    if not drafts:
        print("No Drafts Available.")
        return

    view_drafts()
    index = int(input("\nEnter Draft Number to Delete: ")) - 1

    if 0 <= index < len(drafts):
        drafts.pop(index)
        save_drafts(drafts)
        print("Draft Deleted Successfully.")
    else:
        print("Invalid Draft Number.")

# Send Draft Later
def send_draft_later():
    drafts = load_drafts()

    if not drafts:
        print("No Drafts Available.")
        return

    view_drafts()
    index = int(input("\nEnter Draft Number to Send: ")) - 1

    if 0 <= index < len(drafts):
        drafts[index]["status"] = "Sent"
        save_drafts(drafts)

        print("\nSending Email...")
        print("To :", drafts[index]["recipient"])
        print("Subject :", drafts[index]["subject"])
        print("Message :", drafts[index]["message"])
        print("Email Sent Successfully.")
    else:
        print("Invalid Draft Number.")

# Main Menu
while True:
    print("\n========== Draft Management ==========")
    print("1. Save Draft")
    print("2. View Draft")
    print("3. Edit Draft")
    print("4. Delete Draft")
    print("5. Send Draft Later")
    print("6. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        save_draft()

    elif choice == "2":
        view_drafts()

    elif choice == "3":
        edit_draft()

    elif choice == "4":
        delete_draft()

    elif choice == "5":
        send_draft_later()

    elif choice == "6":
        print("Thank You!")
        break

    else:
        print("Invalid Choice.")