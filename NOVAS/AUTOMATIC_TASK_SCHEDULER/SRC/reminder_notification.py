import csv
import winsound
from datetime import datetime, timedelta
from plyer import notification
import time

notify = "Sound"
shown_tasks = set()

def notify_type():
    global notify

    print("1. Sound")
    print("2. Silent")

    choice = input("Enter choice: ")

    if choice == "1":
        notify = "Sound"
    else:
        notify = "Silent"

def check_reminders():

    print("Reminder service started...")

    while True:

        current_datetime = datetime.now()

        try:
            with open("tasks.csv", "r", newline="") as file:

                reader = csv.DictReader(file)

                for row in reader:

                    task_datetime = datetime.strptime(
                        row["Date"] + " " + row["Time"],
                        "%Y-%m-%d %I:%M %p"
                    )

                    task_key = row["Task ID"]

                    if (
                        task_datetime <= current_datetime <
                        task_datetime + timedelta(minutes=1)
                        and task_key not in shown_tasks
                    ):

                        shown_tasks.add(task_key)

                        print("\n******** TASK REMINDER ********")
                        print("Task :", row["Task Name"])

                        notification.notify(
                            title="Task Reminder",
                            message=f"{row['Task Name']} is due now!",
                            timeout=10
                        )

                        if notify == "Sound":
                            winsound.Beep(1000, 500)

        except FileNotFoundError:
            pass

        time.sleep(30)