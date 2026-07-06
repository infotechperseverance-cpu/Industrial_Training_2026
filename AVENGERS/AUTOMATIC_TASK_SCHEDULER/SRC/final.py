import csv
from gettext import install
import os
import smtplib
from statistics import mode
import time
import threading 
from datetime import datetime, timedelta 
from email.mime.text import MIMEText
from plyer import notification
import speech_recognition as sr
import asyncio
import importlib

# Import edge_tts dynamically to avoid static analysis import errors in
# environments where the package is not installed.
try:
    edge_tts = importlib.import_module("edge_tts")
    EDGE_TTS_AVAILABLE = True
except Exception:
    edge_tts = None
    EDGE_TTS_AVAILABLE = False


USER_FILE = "user.csv"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password", "email"])


def authentication():

    username = input("Enter Username: ")
    password = input("Enter Password: ")
    email = input("Enter Email: ")

    with open(USER_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if (row["username"] == username and
                row["password"] == password and
                row["email"] == email):

                print(f"\nWelcome {username}")
                return email

    print("Invalid Username, Password or Email")
    return None

File_name = 'Tasks.csv'
Completed_file = 'completed.csv'
history_file = 'task_history.csv'
deleted_task = None
sender_email = 'divyapatil1878@gmail.com'
app_pass = 'ynfm tgyl yxyz snxw'
receiver_email = '' 

VOICE = "en-US-AriaNeural"

# Create CSV file

if not os.path.exists(File_name):
    with open(File_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Task_ID","Task_Name","Task_Date","Task_Time","Task_Recurring","Task_Status"])
        
# create history File

if not os.path.exists(history_file):
    with open(history_file, "w", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow(["Task_ID", "Task_Name", "Action", "Status", "Date_Time"])        

def voice_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text

    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""

    except sr.RequestError:
        print("Speech service unavailable")
        return ""
# Add Task

def add_task():
    print("1. Type Through Keyboard")
    print("2. Voice Command")

    mode = input("Choose an option: ")

    if mode == "1": 
        Task_ID = input("Enter a Task ID: ")
        Task_Name = input("Enter a Task Name: ")
        Task_Date = input("Enter Task Date (DD/MM/YYYY): ")
        Task_Time = input("Enter Task Time (HH:MM AM/PM): ").strip()
        print(repr(Task_Time))
        Task_Recurring = input("Task Recurring (Daily/Weekly/Monthly/None): ")
        Task_Status = input("Task Status (Pending/Completed/Failed): ")
    
    elif mode == "2":
        print("Speak Task ID")
        Task_ID = voice_command() # type: ignore

        print("Speak Task Name")
        Task_Name = voice_command()

        print("Speak Task Date")
        Task_Date = voice_command()

        print("Speak Task Time")
        Task_Time = voice_command()
        if not Task_Time:
            print("Could not recognize Task Time")
            return

        Task_Time = Task_Time.upper()

        print("Speak Task Recurring")
        Task_Recurring = voice_command()

        print("Speak Task Status")
        Task_Status = voice_command()

    else:
        print("Invalid Choice")
        return

    if Task_ID == "" or Task_Name == "" or Task_Date == "" or Task_Time == "" or Task_Recurring == "" or Task_Status == "":
        print("Error: All fields are required!")
        return
    
    with open(File_name, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
         if row and row[0] == Task_ID:
            print("Task ID already exists!")
            return
    
    
    try:
        datetime.strptime(Task_Time,"%I:%M %p")
    except ValueError:
        print("Error:Invalid Time")
        return

    try:
        datetime.strptime(Task_Date, "%d/%m/%Y")
    except ValueError:
        print("Error: Invalid date")
        return

    with open(File_name, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([Task_ID, Task_Name, Task_Date, Task_Time, Task_Recurring, Task_Status])
        
    with open(history_file, "a", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow([Task_ID, Task_Name, "Created", Task_Status,
                         datetime.now().strftime("%d/%m/%Y %I:%M %p")])    
            
    print("Task added Successfully")

# Update Task

def update_task():
    Task_ID = input("Enter Task ID for Update: ")
    rows = []
    Task_Name = ""
    Task_Status = ""

    found = False

    with open(File_name, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == Task_ID:
                row[1] = input("Enter New Task Name: ")
                row[2] = input("Enter New Date (DD/MM/YYYY) :")
                row[3] = input("Enter New Time (HH:MM AM/PM): ").strip()
                row[4] = input("Enter Recurring (Daily/Weekly/Monthly/None): ")
                row[5] = input("Enter New Status (Pending/Completed/Failed): ")
                try:
                    datetime.strptime(row[3],"%I:%M %p")
                except ValueError:
                    print("Error:Invalid Time")
                    return            

                Task_Name = row[1]
                Task_Status = row[5]
                found = True
            rows.append(row)

    with open(File_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
        
    with open(history_file, "a", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow([Task_ID, Task_Name, "Updated", Task_Status,
                         datetime.now().strftime("%d/%m/%Y %I:%M %p")])
                         

    if found:
        print("Task Updated Successfully!")
    else:
        print("Task ID Not Found!")

# Delete Task
def delete_task():
    global deleted_task
    Task_ID = input("Enter Task ID for Delete: ")
    data = []
    Task_Name = ""
    Task_Status = ""
    found = False

    with open(File_name, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] !=Task_ID:
                data.append(row)
            else:
                deleted_task = row
                Task_Name = row[1]
                Task_Status = row[5]
                found = True

    with open(File_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
        
    with open(history_file, "a", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow([Task_ID, Task_Name, "Deleted", Task_Status,
                         datetime.now().strftime("%d/%m/%Y %I:%M %p")])
                         

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
            
        with open(history_file, "a", newline="") as hf:
            writer = csv.writer(hf)
            writer.writerow([deleted_task[0], deleted_task[1], "Undo Delete", deleted_task[5],
                         datetime.now().strftime("%d/%m/%Y %I:%M %p")])    

        print("Task Restored Successfully!")

        deleted_task = None
    else:
        print("No Deleted Task Found!")
        
def complete_task():
    
    Task_ID = input("Enter Task ID :")
    tasks = []
    found = False

    if not os.path.exists(Completed_file):
        with open(Completed_file, "w", newline="") as cf:
            writer = csv.writer(cf)
            writer.writerow(["Task_ID", "Task_Name", "Task_Date", "Task_Time", "Task_Recurring", "Task_Status"])

    with open(File_name, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Task_ID"] == Task_ID:
                found = True
                with open(Completed_file, "a", newline="") as cf:
                    writer = csv.writer(cf)
                    row["Task_Status"] = "Completed"
                    writer.writerow([
                        row["Task_ID"],
                        row["Task_Name"],
                        row["Task_Date"],
                        row["Task_Time"],
                        row["Task_Recurring"],
                        row["Task_Status"]
                    ])
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

# View Task

def view_task():
    with open(File_name, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
        if len(rows) <= 1:
            print("No Tasks Available!")
        else:
            for row in rows[1:]:
                for cell in row:
                    print(cell, end="\t")
                print("-"*30) 
                
def dashboard():
    
    total = 0
    completed = 0
    pending = 0
    upcoming = 0
    Failed = 0
    today = datetime.now()

    with open(File_name, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            task_datetime = datetime.strptime(
                row["Task_Date"] + " " + row["Task_Time"],
                "%d/%m/%Y %I:%M %p"
            )
            if row["Task_Status"] == "Pending":
                pending += 1

            elif row["Task_Status"] == "Failed":
                Failed += 1

    if os.path.exists(Completed_file):
        with open(Completed_file, "r") as cf:
          reader = csv.DictReader(cf)
          for row in reader:
            completed += 1

    print("\n===== DASHBOARD =====")
    print("Total Tasks     :", total)
    print("Completed Tasks :", completed)
    print("Pending Tasks   :", pending)
    print("Upcoming Tasks  :", upcoming)
    print("Failed Tasks    :", Failed)     
    
def view_history():
    
    try:
        with open(history_file, "r", newline="") as hf:
            reader = csv.reader(hf)
            
            print("--------- TASK HISTORY ------------\n")
            for i in reader:
                print(*i,sep="\t")
                
    except FileNotFoundError:
        print("No task history found.")

 
def sort_task():

    tasklist = []

    with open(File_name, "r", newline="") as f:
        reader = csv.reader(f)

        for row in reader:
            tasklist.append(row)

    header = tasklist[0]
    tasks = tasklist[1:]

    tasks.sort(
        key=lambda task: datetime.strptime(
            task[2] + " " + task[3],
            "%d/%m/%Y %I:%M %p"
        )
    )

    print("\n----- SORTED TASKS -----")

    print(*header, sep="\t")

    for task in tasks:
        print(*task, sep="\t")

        

def send_email(subject, message):
    print("Sending email to:", receiver_email)
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
        print("Email Error:", e)

async def speak(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("voice.mp3")
    os.system("start voice.mp3")

def speak_task(task_name):
    try:
        asyncio.run(speak(f"Reminder. {task_name}"))
    except Exception as e:
        print("Voice Error:", e)


def show_popup(title, message, task_name=""):

    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

    if task_name:
        threading.Thread(
            target=speak_task,
            args=(task_name,),
            daemon=True
        ).start()


def update_status(task_id, new_status):

    rows = []

    with open(File_name, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["Task_ID"] == str(task_id):
                row["Task_Status"] = new_status

            rows.append(row)

    with open(File_name, "w", newline="") as f:
        writer = csv.DictWriter(f,fieldnames=["Task_ID", "Task_Name", "Task_Date", "Task_Time", "Task_Recurring", "Task_Status"])

        writer.writeheader()
        writer.writerows(rows)


def email_notification():

    current_time = datetime.now()

    with open(File_name, "r", newline="") as f:

        reader = csv.DictReader(f)
        for row in reader:

            try:
                task_time = datetime.strptime(row["Task_Date"] + " " + row["Task_Time"], "%d/%m/%Y %I:%M %p") 

                status = row["Task_Status"]

                # 10 Minute Reminder
                if (status == "Pending" and task_time > current_time and task_time - current_time <= timedelta(minutes=10)):

                    msg = f"""
                    Task : {row['Task_Name']}
                    Date : {row['Task_Date']}
                    Time : {row['Task_Time']}

                    Your task will start in 10 minutes.
                    """

                    show_popup("Task Reminder", msg, row["Task_Name"])
                    send_email("Task Reminder", msg)

                    update_status(row["Task_ID"], "Reminder Sent" )

                # On Time Notification
                elif (status in ["Pending", "Reminder Sent"] and abs((task_time - current_time).total_seconds()) <= 60):
                    msg = f"""
                    Task : {row['Task_Name']}
                    Date : {row['Task_Date']}
                    Time : {row['Task_Time']}

                    It's time to complete your task.
              """

                    show_popup("Task Started", msg, row["Task_Name"])
                    send_email("Task Started", msg)

                    update_status(row["Task_ID"], "Started")

                # Missed Task
                elif (status == "Started" and current_time > task_time + timedelta(minutes=5)):

                    msg = f"""
                   You missed your scheduled task.

                Task : {row['Task_Name']}
                 """

                    show_popup("Task Failed", msg, row["Task_Name"])
                    send_email("Task Failed", msg)

                    update_status(row["Task_ID"], "Failed" )

            except Exception as e:
                print("Task Error:", e)


def notification_loop():

    while True:

        try:
            email_notification()

        except Exception as e:
            print("Notification Error:", e)

        time.sleep(60)

thread = threading.Thread(target=notification_loop, daemon=True)

thread.start()
print("Notification Service Started...")
                

# Main Menu
receiver_email = authentication()

if not receiver_email:
    print("Login Failed")
    exit()

print("Logged in Email:", receiver_email)

while True:
    print("\\n----- Task Management -----")

    print("1. Add Task")
    print("2. Update Task")
    print("3. Delete Task")
    print("4. Undo Delete Task")
    print("5. Completed")
    print("6. View Tasks")
    print("7. Dashboard ")
    print("8. view history")
    print("9. Sort Tasks")
    print("10.Exit")

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
            complete_task()
        case 6:
            view_task()
        case 7:
            dashboard()
        case 8:
            view_history()
        case 9:
            sort_task()
        case 10:
            print("Thank You!")
            break
        case _:
            print("Invalid Choice!")