from datetime import datetime, timedelta
from plyer import notification
import winsound
import csv
import time

remainder_list = []
shown_reminders = set()

def Take_remainder_interval():

    global remainder_list

    remainder_list.clear()

    print("Available reminder intervals:")
    print("5, 10, 15, 30")

    intervals = input(
        "Enter reminder intervals (comma separated): "
    )

    for i in intervals.split(","):

        try:
            value = int(i.strip())

            if value in [5, 10, 15, 30]:
                remainder_list.append(value)

        except ValueError:
            pass

    print("Saved:", remainder_list)

def set_remainder():

    while True:

        current_time = datetime.now()

        try:
            with open("tasks.csv", "r", newline="") as file:

                reader = csv.DictReader(file)

                for row in reader:

                    task_datetime = datetime.strptime(
                        row["Date"] + " " + row["Time"],
                        "%Y-%m-%d %I:%M %p"
                    )

                    for interval in remainder_list:

                        reminder_time = (
                            task_datetime -
                            timedelta(minutes=interval)
                        )

                        key = (
                            f"{row['Task_ID']}_{interval}"
                        )

                        if (
                            reminder_time <= current_time <
                            reminder_time + timedelta(minutes=1)
                            and key not in shown_reminders
                        ):

                            shown_reminders.add(key)

                            notification.notify(
                                title="Upcoming Task",
                                message=(
                                    f"{row['Task Name']} "
                                    f"starts in {interval} minutes"
                                ),
                                timeout=10
                            )

                            winsound.Beep(1000, 500)

        except FileNotFoundError:
            pass

        time.sleep(30)