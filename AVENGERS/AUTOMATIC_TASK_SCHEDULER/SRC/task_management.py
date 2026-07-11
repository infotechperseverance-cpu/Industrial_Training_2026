import csv
import os
from datetime import datetime
import threading 
from Notification import start_notification
File_name = "Tasks.csv"
deleted_task = None

# Create CSV file

if not os.path.exists(File_name):
    with open(File_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Task_ID", "Task_Name", "Task_Date", "Task_Time", "Task_Recurring"])

# Add Task

def add_task():
    task_ID = input("Enter a Task ID: ")
    task_name = input("Enter a Task Name: ")
    task_date = input("Enter Task Date (DD/MM/YYYY): ")
    task_time = input("Enter Task Time (HH:MM AM:PM): ")
    task_recurring = input("Task Recurring (Daily/Weekly/Monthly/None): ")

    if task_ID == "" or task_name == "" or task_date == "" or task_time == "" or task_recurring == "":
        print("Error: All fields are required!")
        return

    try:
        datetime.strptime(task_date, "%d/%m/%Y")
    except ValueError:
        print("Error: Invalid date")
        return

    with open(File_name, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            f"Task_ID: {task_ID}",
            f"Task_Name: {task_name}",
            f"Task_Date: {task_date}",
            f"Task_Time: {task_time}",
            f"Task_Recurring: {task_recurring}"])

    print("Task added Successfully")

# Update Task

def update_task():
    task_ID = input("Enter Task ID for Update: ")
    rows = []

    found = False

    with open(File_name, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == f"Task_ID: {task_ID}":
                row[1] = f"Task_Name: {input('Enter New Task Name: ')}"
                row[2] = f"Task_Date: {input('Enter New Date: ')}"
                row[3] = f"Task_Time: {input('Enter New Time: ')}"
                row[4] = f"Task_Recurring: {input('Enter Recurring (Daily/Weekly/Monthly/None): ')}"

                found = True
            rows.append(row)

    with open(File_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    if found:
        print("Task Updated Successfully!")
    else:
        print("Task ID Not Found!")

# Delete Task
def delete_task():
    global deleted_task
    task_ID = input("Enter Task ID for Delete: ")
    data = []
    found = False

    with open(File_name, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != f"Task_ID: {task_ID}":
                data.append(row)
            else:
                deleted_task = row
                found = True

    with open(File_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    if found:
        print("Task Deleted Successfully!")
    else:
        print("Task ID Not Found!")

# Undo Delete

def undo_delete():

    global deleted_task

    if deleted_task:
        with open(File_name, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(deleted_task)

        print("Task Restored Successfully!")

        deleted_task = None
    else:
        print("No Deleted Task Found!")

# View Task

def view_task():
    with open(File_name, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
        if len(rows) <= 1:
            print("No Tasks Available!")
        else:
            for row in rows[1:]:
                for i in row:
                    print(i)
                print("-"*30)  

# Main Menu

def task_management():
    while True:
        print("\n----- Task Management -----")

        print("1. Add Task")
        print("2. Update Task")
        print("3. Delete Task")
        print("4. Undo Delete Task")
        print("5. View Tasks")
        print("6. Exit")

        print("*"*30)

        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        match choice:
            case 1:
                add_task()
            case 2:
                update_task()
            case 3:
                delete_task()
            case 4:
                undo_delete()
            case 5:
                view_task()
            case 6:
                print("Thank You!")
                break
            case _:
                print("Invalid Choice!")
    
    if __name__ == "__main__":
        print("Starting Notification Scheduler...")

        threading.Thread(target=start_notification, daemon=True).start()
        task_management()