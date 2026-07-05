import os
import json
import matplotlib.pyplot as plt

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
    emails = load_email_records()

    if len(emails) == 0:
        print("No Email Records Found")
        return

    completed = 0
    failed = 0
    scheduled = 0

    for email in emails:

        status = email.get("status", "").lower().strip()
        
        if status == "completed":
            completed += 1
        elif status == "failed":
            failed += 1
        elif status == "scheduled":
            scheduled += 1

    labels = []
    values = []

    if completed > 0:
        labels.append("Completed")
        values.append(completed)

    if failed > 0:
        labels.append("Failed")
        values.append(failed)

    if scheduled > 0:
        labels.append("Scheduled")
        values.append(scheduled)


    if not values:
        print("No valid email statuses (Completed/Failed/Scheduled) found to generate a chart.")
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

