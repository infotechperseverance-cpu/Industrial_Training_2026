import os
import json
import matplotlib.pyplot as plt
<<<<<<< HEAD
=======
from voice import speak
>>>>>>> fc73ecbf6f619b0e3d24852bc80ccf70027f2541

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
<<<<<<< HEAD
=======

    speak("-----------Pie Chart---------")
    
>>>>>>> fc73ecbf6f619b0e3d24852bc80ccf70027f2541
    emails = load_email_records()

    if len(emails) == 0:
        print("No Email Records Found")
        return

    completed = 0
<<<<<<< HEAD
    failed = 0
    scheduled = 0
=======
    pending = 0
    spam = 0
>>>>>>> fc73ecbf6f619b0e3d24852bc80ccf70027f2541

    for email in emails:

        status = email.get("status", "").lower().strip()
        
        if status == "completed":
            completed += 1
<<<<<<< HEAD
        elif status == "failed":
            failed += 1
        elif status == "scheduled":
            scheduled += 1
=======
        elif status == "pending":
            pending += 1
        elif status == "spam":
            spam += 1
>>>>>>> fc73ecbf6f619b0e3d24852bc80ccf70027f2541

    labels = []
    values = []

    if completed > 0:
        labels.append("Completed")
        values.append(completed)

<<<<<<< HEAD
    if failed > 0:
        labels.append("Failed")
        values.append(failed)

    if scheduled > 0:
        labels.append("Scheduled")
        values.append(scheduled)


    if not values:
        print("No valid email statuses (Completed/Failed/Scheduled) found to generate a chart.")
=======
    if pending > 0:
        labels.append("Pending")
        values.append(pending)

    if spam > 0:
        labels.append("spam")
        values.append(spam)


    if not values:
        print("No valid email statuses (Completed/Pending/Spam) found to generate a chart.")
>>>>>>> fc73ecbf6f619b0e3d24852bc80ccf70027f2541
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

