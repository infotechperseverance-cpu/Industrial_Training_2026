import os
import csv
import time
import smtplib
from datetime import datetime
import schedule
from plyer import notification
from datetime import datetime, timedelta
from email.mime.text import MIMEText
File_name = "Tasks.csv"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
File_name = os.path.join(BASE_DIR, "Tasks.csv")

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
                row["Date"] + " " + row["Time"],
                "%d-%m-%Y %H:%M:%S"
            )

            if(row["Status"].strip() == "Pending" and task_time > current_time and task_time - current_time <= timedelta(minutes=10)): 
                send_email(
                    "Task Reminder",
                    "Your task will start in 10 minutes.\n"

                    f'''Task: {row['Task']}\n
                        Date: {row['Date']}\n
                        Time: {row['Time']}\n

                    Complete your task on time.'''
                )


            elif row["Status"].strip() == "Failed":
                send_email(
                    "Task Failed",
                    f'''You missed your scheduled task.\n

                    Task: {row['Task']}'''
                )
                row["Status"] = "Email Sent"
            rows.append(row)
        with open(File_name, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Task", "Date", "Time", "Status"])
            writer.writeheader()
            writer.writerows(rows)
            
def setup_scheduler():
	if os.path.exists("Tasks.csv"):
		with open("Tasks.csv", "r", newline="") as taskfile:
			timereader = csv.reader(taskfile)
 			for row in timereader:
			task_title = row[0]
			target_time = row[2]
			schedule.every().day.at(target_time).do(send_popup, task_title=task_title)
setup_scheduler()
print("Notification scheduler is running...")
while True:
	schedule.run_pending()
	time.sleep(1)
    if os.path.exists(File_name):
        with open(File_name, "r", newline="") as taskfile:
            timereader = csv.reader(taskfile, skipinitialspace=True)
            next(timereader)   # Skip header

            for row in timereader:
                task_title = row[0].strip()
                target_time = row[2].strip()
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
