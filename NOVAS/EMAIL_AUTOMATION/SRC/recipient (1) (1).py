import json
import csv
import os
from datetime import datetime

FILE_NAME = "recipients.json"


def load():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)

            if isinstance(data, list):
                return data
            else:
                return []

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save(recipients):
    with open(FILE_NAME, "w") as f:
        json.dump(recipients, f, indent=4)


def check_email(email):
    if "@" in email and ".com" in email:
        return True
    return False        


def add_recipient():
    try:
        recipients = load()

        name = input("Enter Name: ")

        email = input("Enter Recipient Email: ")
        if not check_email(email):
            print("Invalid Email!")
            email = input("enter email")

        subject = input("Enter Subject: ")
        message = input("Enter Message: ")

        schedule_date = input("Enter Schedule Date (DD-MM-YYYY): ")
        schedule_time = input("Enter Schedule Time (HH:MM): ")

        schedule = datetime.strptime(schedule_date + " " + schedule_time, "%d-%m-%Y %H:%M")

        if schedule < datetime.now():
            print("Past Date and Time Not Allowed!")
            return

        status = input("Enter Status (Pending/Sent): ")

        recipient = {
            "email_id": len(recipients) + 1,
            "name": name,
            "recipient_email": email,
            "subject": subject,
            "message": message,
            "schedule_date": schedule_date,
            "schedule_time": schedule_time,
            "status": status
        }

        recipients.append(recipient)
        save(recipients)
        print("Recipient Added Successfully!")

    except ValueError:
        print("Invalid Time or date Format")

    except:
        print("something went wrong")


def add_multiple():
    recipients = load()

    while True:
        name = input("Enter Name: ")

        email = input("Enter Recipient Email: ")
        if not check_email(email):
            print("Invalid Email!")
            continue

        subject = input("Enter Subject: ")
        message = input("Enter Message: ")

        schedule_date = input("Enter Schedule Date (DD-MM-YYYY): ")
        schedule_time = input("Enter Schedule Time (HH:MM): ")

        schedule = datetime.strptime(schedule_date + " " + schedule_time, "%d-%m-%Y %H:%M")

        if schedule < datetime.now():
            print("Past Date and Time Not Allowed!")
            continue

        status = input("Enter Status (Pending/Sent): ")

        recipient = {
            "email_id": len(recipients) + 1,
            "name": name,
            "recipient_email": email,
            "subject": subject,
            "message": message,
            "schedule_date": schedule_date,
            "schedule_time": schedule_time,
            "status": status
        }

        recipients.append(recipient)

        choice = input("Add Another Recipient? (yes/no): ")
        if choice.lower() == "no":
            break

    save(recipients)
    print("Recipients Added Successfully!")



def create_group():
    group = input("Enter Group Name: ")
    print("Group", group, "Created Successfully!")


def edit_recipient():
    recipients = load()

    rid = int(input("Enter Email ID: "))

    for recipient in recipients:
        if recipient["email_id"] == rid:

            recipient["name"] = input("Enter New Name: ")

            email = input("Enter New Recipient Email: ")
            if not check_email(email):
                print("Invalid Email!")
                return
            recipient["recipient_email"] = email

            recipient["subject"] = input("Enter New Subject: ")
            recipient["message"] = input("Enter New Message: ")

            schedule_date = input("Enter New Schedule Date (DD-MM-YYYY): ")
            schedule_time = input("Enter New Schedule Time (HH:MM): ")

            schedule = datetime.strptime(schedule_date + " " + schedule_time, "%d-%m-%Y %H:%M")

            if schedule < datetime.now():
                print("Past Date and Time Not Allowed!")
                return

            recipient["schedule_date"] = schedule_date
            recipient["schedule_time"] = schedule_time
            recipient["status"] = input("Enter New Status: ")

            save(recipients)
            print("Recipient Updated Successfully!")
            return

    print("Recipient Not Found!")


def delete_recipient():
    recipients = load()

    rid = int(input("Enter Email ID: "))

    for recipient in recipients:
        if recipient["email_id"] == rid:
            recipients.remove(recipient)
            save(recipients)
            print("Recipient Deleted Successfully!")
            return

    print("Recipient Not Found!")


while True:
    print("\n1. Add Recipient")
    print("2. Add Multiple Recipients")
    print("3. Create Recipient Group")
    print("4. Edit Recipient")
    print("5. Delete Recipient")
    print("6. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_recipient()

    elif choice == "2":
        add_multiple()

    elif choice == "3":
        create_group()

    elif choice == "4":
        edit_recipient() 

    elif choice == "5":
        delete_recipient()

    elif choice == "6":
        print("Thank You!")
        break

    else:
        print("Invalid Choice!")
