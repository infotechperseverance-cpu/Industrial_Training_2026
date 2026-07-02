import csv
from datetime import datetime, date

'''---------- SYSTEM RECORDS TASK CREATION TIMESTAMP ----------'''

def record_creation(task):
    now = datetime.now()
    task.created_date = now.strftime("%d-%m-%Y")
    task.created_time = now.strftime("%I:%M %p")


'''---------- SYSTEM RECORDS TASK COMPLETION TIMESTAMP ----------'''

def record_completion(task):
    task.Status = "Completed"
    now = datetime.now()
    task.completed_date = now.strftime("%d-%m-%Y")
    task.completed_time = now.strftime("%I:%M %p")


'''---------- VIEW TASKS DUE TODAY ----------'''

def view_tasks_due_today():

    today = date.today().strftime("%d-%m-%Y")

    print("\n---------- TASKS DUE TODAY ----------")

    found = False

    with open("tasks.csv", "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Date"] == today:

                print(
                    row["Task_ID"], "|",
                    row["Title"], "|",
                    row["Date"], "|",
                    row["Time"], "|",
                    row["Priority"], "|",
                    row["Status"]
                )

                found = True

    if not found:
        print("No tasks due today.")


'''---------- VIEW OVERDUE TASKS ----------'''

def view_overdue_tasks():

    today = datetime.now()

    print("\n---------- OVERDUE TASKS ----------")

    found = False

    with open("tasks.csv", "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            task_date = datetime.strptime(row["Date"], "%Y-%m-%d")

            if task_date < today and row["Status"].lower() != "completed":

                print(
                    row["Task ID"], "|",
                    row["Task Name"], "|",
                    row["Date"], "|",
                    row["Time"], "|",
                    row["Priority"], "|",
                    row["Status"]
                )

                found = True

    if not found:
        print("No overdue tasks.")