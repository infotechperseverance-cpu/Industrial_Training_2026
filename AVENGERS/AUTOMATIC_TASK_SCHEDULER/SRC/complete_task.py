import csv
import os

Completed_file = "completed.csv"

def complete_task():
    task_ID = input("Enter Task ID :")
    tasks = []
    found = False

    if not os.path.exists(Completed_file):
        with open(Completed_file, "w", newline="") as cf:
            writer = csv.writer(cf)
            writer.writerow(["Task_ID", "Task_Name", "Task_Date", "Task_Time", "Task_Recurring"])

    with open(File_name, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Task_ID"] == task_ID:
                found = True
                with open(Completed_file, "a", newline="") as cf:
                    writer = csv.writer(cf)
                    writer.writerow([
                        row["Task_ID"],
                        row["Task_Name"],
                        row["Task_Date"],
                        row["Task_Time"],
                        row["Task_Recurring"]
                    ])
            else:
                tasks.append(row)

    if found:
        with open(File_name, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["Task_ID", "Task_Name", "Task_Date", "Task_Time", "Task_Recurring"]
            )
            writer.writeheader()
            writer.writerows(tasks)
        print("Task Completed Successfully.")
    else:
        print("Task ID Not Found.")

complete_task()
