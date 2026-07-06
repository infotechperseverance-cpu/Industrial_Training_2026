import csv
import os
from datetime import datetime
import threading 
import time
import smtplib
import schedule
from plyer import notification
from datetime import datetime, timedelta
from email.mime.text import MIMEText

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

File_name = os.path.join(BASE_DIR, "Tasks.csv")
Completed_file = os.path.join(BASE_DIR, "completed.csv")
deleted_task = None 

if not os.path.exists("user.csv"):
    with open("user.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username","password"])

def authentication():
    username = input("Enter username: ")
    password = input("Enter password: ")
    login_success = False
    existing_user = False
    with open("user.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username:
                existing_user = True
                if row["password"] == password:
                    login_success = True
                    break
    if login_success:
        print("Login successful!")
    elif existing_user:
        print("Invalid password")
    else:
        print("user does not exist. Creating new account")
        with open('user.csv', 'a', newline='') as csvfile:
            userwriter = csv.writer(csvfile, delimiter=',')
            userwriter.writerow([username, password])
            print("user created")
      
# Create CSV file

if not os.path.exists(File_name):
    with open(File_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Task_ID", "Task_Name", "Task_Date", "Task_Time", "Task_Recurring", "Task_Status"])

# Add Task

def add_task():
    Task_ID = int(input("Enter Task ID :").strip())
    Task_name = input("Enter a Task Name: ")
    Task_date = input("Enter Task Date (YYYY-MM-DD): ")
    Task_time = input("Enter Task Time (HH:MM:SS): ")
    Task_recurring = input("Task Recurring (Daily/Weekly/Monthly/None): ")
    Task_status = input("Task Status (Pending/In Progress/Completed): ")

    if Task_ID == 0 or Task_name == "" or Task_date == "" or Task_time == "" or Task_recurring == "" or Task_status == "":
        print("Error: All fields are required!")
        return

    try:
       datetime.strptime(Task_date, "%Y-%m-%d")
    except ValueError:
       print("Error: Invalid date")
       return

    with open(File_name, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            Task_ID,
            Task_name,
            Task_date,
            Task_time,
            Task_recurring,
            Task_status
     ])
    print("Task added Successfully")

# Update Task

def update_task():
    Task_ID = int(input("Enter Task ID for Update: "))
    rows = []

    found = False

    with open(File_name, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Task_ID"] == str(Task_ID):
                row["Task_Name"] = input("Enter New Task Name: ")
                row["Task_Date"] = input("Enter New Date: ")
                row["Task_Time"] = input("Enter New Time: ")
                row["Task_Recurring"] = input("Enter Recurring (Daily/Weekly/Monthly/None): ")
                row["Task_Status"] = input("Enter New Status (Pending/Failed/Completed): ")
                found = True
            rows.append(row)

    with open(File_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        writer.writeheader()
        writer.writerows(rows)

    if found:
        print("Task Updated Successfully!")
    else:
        print("Task ID Not Found!")

# Delete Task
def delete_task():
    Task_ID = int(input("Enter Task ID to delete: ").strip())
    global deleted_task
    rows = []
    found = False

    with open(File_name, "r", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            print("No tasks file or file is empty")
            return

        for row in reader:
            # skip empty lines
            if not row:
                continue
            if row[0].strip() == str(Task_ID):
                found = True
                # store deleted task as dict for undo
                deleted_task = {header[i]: row[i] for i in range(len(header))}
                continue
            rows.append(row)

    with open(File_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    if found:
        print("Task Deleted")
    else:
        print("Task ID Not Found")
# Undo Delete

def undo_delete():

    global deleted_task

    if deleted_task:
        with open(File_name, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=deleted_task.keys())
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
        print("6. Dashboard")
        print("7. Complete Task")   
        print("8. Prioritize Tasks")
        print("9. Exit")    

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
                dashboard()
            case 7:
                complete_task() 
            case 8:
                prioritize()
            case 9:
                print("Thank you!!")
                break
            case _:
                print("Invalid Choice!")

               
tasklist = []

with open(File_name, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
          tasklist.append(row)

def sort_task_by_status():
   with open("completedTasks.csv", "w", newline="") as completefile, \
      open("pendingTasks.csv", "w", newline="") as pendingfile, \
      open("failedTasks.csv", "w", newline="") as failedfile:
      completewrite = csv.DictWriter(completefile, fieldnames=tasklist[0].keys() if tasklist else [])
      pendingwrite = csv.DictWriter(pendingfile, fieldnames=tasklist[0].keys() if tasklist else [])
      failedwrite = csv.DictWriter(failedfile, fieldnames=tasklist[0].keys() if tasklist else [])

      completewrite.writeheader()
      pendingwrite.writeheader()
      failedwrite.writeheader()

      for task in tasklist:
         status = task["Task_Status"].strip().lower()
         if status == "completed":
           completewrite.writerow(task)
         elif status == "pending":
           pendingwrite.writerow(task)
         else:
           failedwrite.writerow(task)

import csv
from datetime import datetime

def prioritize():
    tasklist = []

    
    with open("prioritized.csv", "w", newline="") as priorityfile:
        writer = csv.writer(priorityfile)

        writer.writerow([
           "Task_ID",
           "Task_Name",
           "Task_Date",
           "Task_Time",
           "Task_Recurring",
           "Task_Status"
       ])

        writer.writerows(tasklist)

    
    tasklist.sort(
        key=lambda task: datetime.strptime(
            task["Task_Date"] + " " + task["Task_Time"],
            "%Y-%m-%d %H:%M:%S"
        )
    )

    with open("prioritized.csv", "w", newline="") as priorityfile:
        writer = csv.DictWriter(priorityfile, fieldnames=tasklist[0].keys() if tasklist else [])

        # header (optional but good)
        writer.writeheader()

        for task in tasklist:
            writer.writerow(task)


def complete_task():
    Task_ID = int(input("Enter Task ID : ").strip())
    tasks = []
    found = False
    

    print("Tasks file", Tasks.csv)
    print("Completed file", Completed_file)
    print("Absolute Path:", os.path.abspath(Completed_file))

    if not os.path.exists(Completed_file):
        with open(Completed_file, "w", newline="") as cf:
            writer = csv.DictWriter(cf, fieldnames=["Task_ID", "Task_Name", "Task_Date", "Task_Time", "Task_Recurring"])
            writer.writeheader()

    with open(File_name, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            if int(row["Task_ID"]) == Task_ID:
                print("Matched Task:", row)
                with open(Completed_file, "a", newline="") as cf:
                    writer = csv.writer(cf)
                    writer.writerow([
                        row["Task_ID"],
                         row["Task_Name"],
                         row["Task_Date"],
                         row["Task_Time"],
                         row["Task_Recurring"],
                         row["Task_Status"]
                        ])

                    cf.flush()

                print("Row Written")
                print("Stored in completed.csv")
                found = True
            else:
                tasks.append(row)

    if found:
        with open(File_name, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["Task_ID", "Task_Name", "Task_Date", "Task_Time", "Task_Recurring", "Task_Status"]
            )
            writer.writeheader()
            writer.writerows(tasks)
        print("Task Completed Successfully.")
    else:
        print("Task ID Not Found.")




sender_email = "divyapatil1878@gmail.com"
app_pass = "aott lbvr ladm ntaa"
receiver_email = "divyapatil1878@gmail.com"	


def send_popup(task_title):
	notification.notify(title="Task Reminder",message=task_title,timeout=10 )

def send_email(subject, message):
    
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_pass)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email Sent Successfully")
    except Exception as e:
        print("Error,plz try again:", e)

def email_notification():
    
    current_time = datetime.now()
    rows = []
    with open(File_name, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task_time = datetime.strptime(
                row["Task_Date"] + " " + row["Task_Time"],
                "%Y-%m-%d %H:%M:%S"
            )

            if(row["Task_Status"].strip() == "Pending" and task_time > current_time and task_time - current_time <= timedelta(minutes=10)): 
                send_email(
                    "Task Reminder",
                    "Your task will start in 10 minutes.\n"

                    f'''Task: {row['Task_Name']}\n
                        Date: {row['Task_Date']}\n
                        Time: {row['Task_Time']}\n

                    Complete your task on time.'''
                )


            elif row["Task_Status"].strip() == "Failed":
                send_email(
                    "Task Failed",
                    f'''You missed your scheduled task.\n

                    Task: {row['Task_Name']}'''
                )
                row["Task_Status"] = "Email Sent"
            rows.append(row)
        with open(File_name, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Task_ID", "Task_Name", "Task_Date", "Task_Time", "Task_Recurring", "Task_Status"])
            writer.writeheader()
            writer.writerows(rows)
            
def setup_scheduler():
    if os.path.exists(File_name):
        with open(File_name, "r", newline="") as taskfile:
            timereader = csv.reader(taskfile, skipinitialspace=True)
            next(timereader)   # Skip header

            for row in timereader:
                task_title = row[0].strip()
                target_time = row[3].strip()
                print(len(target_time), repr(target_time))

                schedule.every().day.at(target_time).do(
                    send_popup,
                    task_title=task_title
                )
def start_notification():
    setup_scheduler()
    print("Notification scheduler is running...")
    while True:
        email_notification()
        schedule.run_pending()
        time.sleep(60)


def dashboard():
    File_name = "Tasks.csv"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    File_name = os.path.join(BASE_DIR, "Tasks.csv")

    total = 0
    completed = 0
    pending = 0
    upcoming = 0
    failed = 0

    today = datetime.now()

    if not os.path.exists(File_name):
        print("Tasks.csv file not found!")
        return

    with open(File_name, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            total += 1

            try:
                task_datetime = datetime.strptime(
                    row["Task_Date"] + " " + row["Task_Time"],
                    "%Y-%m-%d %H:%M:%S"
                )

                if task_datetime > today:
                    upcoming += 1
                    pending += 1
                else:
                    failed += 1

            except Exception as e:
                print("Error in row:", row)
                print("Reason:", e)

    if os.path.exists("completed.csv"):
        with open("completed.csv", "r", newline="") as cf:
            reader = csv.DictReader(cf)

            for row in reader:
                completed += 1

    print("\n===== DASHBOARD =====")
    print("Total Tasks      :", total)
    print("Completed Tasks  :", completed)
    print("Pending Tasks    :", pending)
    print("Upcoming Tasks   :", upcoming)
    print("Failed Tasks     :", failed)

if __name__ == "__main__":

    authentication()

    task_management()
    
    dashboard()

