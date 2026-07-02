import csv
import os
from validation_methods import (
    is_valid_date,
    is_valid_time,
    is_valid_task_name,
    is_valid_category,
    is_valid_priority
)

FILE_NAME = "tasks.csv"

HEADER = ['Task ID', 'Task Name', 'Date', 'Time', 'Priority','Category','Status','Repeat']


# ---------------- GENERATE ID ----------------
def generate_task_id():
    if not os.path.exists(FILE_NAME):
        return 1
    

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        tasks = list(reader)

    return len(tasks) + 1


# ---------------- ADD TASK ----------------
def add_task():


    task_id = generate_task_id()

    while True:
        task_name = input("Enter Task Name: ")
        if is_valid_task_name(task_name):
            break
        print("Invalid Task Name.")

    while True:
        date = input("Enter Date (YYYY-MM-DD): ")
        if is_valid_date(date):
            break
        print("Invalid Date.")

    while True:
        time = input("Enter Time (HH:MM AM/PM): ")
        if is_valid_time(time):
            break
        print("Invalid Time.")

    while True:
        priority = input("Enter Priority (High/Medium/Low): ")
        if is_valid_priority(priority):
            break
        print("Invalid Priority.")

    while True:
        category = input("Enter Category (Work/Study/Personal/Others): ")
        if is_valid_category(category):
            break
        print("Invalid Category.")

    status = "Pending"

    file_exists = os.path.exists(FILE_NAME)

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)

        if not file_exists or os.stat(FILE_NAME).st_size == 0:
            writer.writeheader()

        writer.writerow({
            'Task ID': task_id,
            'Task Name': task_name,
            'Date': date,
            'Time': time,
            'Priority': priority,
            'Category': category,
            'Status': status,
            'Repeat': "None"
        })

    print("Task Added Successfully.")


# ---------------- VIEW TASK ----------------
def view_task():

    if not os.path.exists(FILE_NAME):
        print("No tasks found.")
        return

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        print(os.path.abspath("tasks.csv"))

        found = False

        for task in reader:
            found = True
            print("\n---------Task Details-----------")
            print("Task ID   :", task.get("Task ID"))
            print("Title     :", task.get("Task Name"))
            print("Date      :", task.get("Date"))
            print("Time      :", task.get("Time"))
            print("Priority  :", task.get("Priority"))
            print("Category  :", task.get("Category"))
            print("Status    :", task.get("Status"))
            print("Repeat    :", task.get("Repeat"))
            print("---------------------------------")

        if not found:
            print("No tasks available.")


# ---------------- MARK TASK COMPLETED ----------------
def mark_task_completed():

    task_id = input("Enter Task ID to mark as completed: ")

    tasks = []

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Task ID"] == task_id:
                row["Status"] = "Completed"
                print("Task marked as completed.")

            tasks.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(tasks)