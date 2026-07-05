import os
import json
import matplotlib.pyplot as plt
from voice import speak

EMAIL_FILE = "email_records.json"

def load_email_records():
    if os.path.exists(EMAIL_FILE):
        with open(EMAIL_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def generate_pie_chart():

    speak("-----------Pie Chart---------")
    
    emails = load_email_records()

    if len(emails) == 0:
        print("No Email Records Found")
        return

    completed = 0
    pending = 0
    spam = 0

    for email in emails:

        status = email.get("status", "").lower().strip()
        
        if status == "completed":
            completed += 1
        elif status == "pending":
            pending += 1
        elif status == "spam":
            spam += 1

    labels = []
    values = []

    if completed > 0:
        labels.append("Completed")
        values.append(completed)

    if pending > 0:
        labels.append("Pending")
        values.append(pending)

    if spam > 0:
        labels.append("Spam")
        values.append(spam)


    if not values:
        print("No valid email statuses (Completed/Pending/Spam) found to generate a chart.")
        return

    plt.figure(figsize=(6,6))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Email Status Analytics")
    plt.axis("equal")
    plt.show()


