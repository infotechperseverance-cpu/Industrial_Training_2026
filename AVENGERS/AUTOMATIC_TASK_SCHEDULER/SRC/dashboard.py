from datetime import datetime
import csv

def dashboard():
    total = 0
    completed = 0
    pending = 0
    upcoming = 0
    Failed = 0
    today = datetime.now()

    with open("task.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            task_datetime = datetime.strptime(
                row["Task_Date"] + " " + row["Task_Time"],
                "%d/%m/%Y %I:%M %p"
            )
            if task_datetime > today:
                upcoming += 1
                pending += 1
            else:
                Failed += 1

    with open("completed.csv", "r") as cf:
        reader = csv.DictReader(cf)
        for row in reader:
            completed += 1

    print("\n===== DASHBOARD =====")
    print("Total Tasks :", total)
    print("Completed Tasks :", completed)
    print("Pending Tasks :", pending)
    print("Upcoming Tasks :", upcoming)
    print("Failed Tasks :", Failed)

dashboard()
