import smtplib
import time
import csv
from datetime import datetime, timedelta
from email.mime.text import MIMEText

sender_email = 'sender email'
app_pass = 'password'
receiver_email = 'recevier email'
File_name ="tasks.csv"

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
    
    with open(File_name, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task_time = datetime.strptime(
                row["Task_Date"] + " " + row["Task_Time"],
                "%d/%m/%Y %I:%M %p"
            )

            if task_time > current_time and task_time - current_time <= timedelta(minutes=10):
                send_email(
                    "Task Reminder",
                    "Your task will start in 10 minutes.\n"

                    f'''Task: {row['Task_Name']}\n
                        Date: {row['Task_Date']}\n
                        Time: {row['Task_Time']}\n

                    Complete your task on time.'''
                )

            elif current_time > task_time:
                send_email(
                    "Task Failed",
                    f'''You missed your scheduled task.\n

                    Task: {row['Task_Name']}'''
                )

while True:
    
    email_notification()
    time.sleep(60)
