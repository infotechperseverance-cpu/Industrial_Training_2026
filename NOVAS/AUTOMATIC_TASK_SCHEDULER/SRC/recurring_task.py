import csv
from datetime import datetime, timedelta
import calendar

def recurring_tasks():

    rows = []

    with open("tasks.csv", "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            # Only process completed recurring tasks
            if row["Status"] != "Completed":
                rows.append(row)
                continue

            repeat = row["Repeat"]

            if repeat == "None":
                rows.append(row)
                continue

            task_date = datetime.strptime(
                row["Date"],
                "%Y-%m-%d"
            )

            if repeat == "Daily":
                task_date += timedelta(days=1)

            elif repeat == "Weekly":
                task_date += timedelta(days=7)

            elif repeat == "Monthly":

                month = task_date.month + 1
                year = task_date.year

                if month > 12:
                    month = 1
                    year += 1

                day = min(
                    task_date.day,
                    calendar.monthrange(year, month)[1]
                )

                task_date = task_date.replace(
                    year=year,
                    month=month,
                    day=day
                )

            row["Date"] = task_date.strftime("%Y-%m-%d")
            row["Status"] = "Pending"

            rows.append(row)

    with open("tasks.csv", "w", newline="") as file:

        fieldnames = [
            "Task ID",
            "Task Name",
            "Date",
            "Time",
            "Priority",
            "Category",
            "Status",
            "Repeat"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print("Recurring tasks updated successfully.")