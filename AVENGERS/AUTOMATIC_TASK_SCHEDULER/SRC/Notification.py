import os
import csv
import time
import pyttsx3
import threading
from datetime import datetime
import schedule
from plyer import notification

engine = pyttsx3.init()
engine = setProperty('rate', 160)
engine = setProperty('volume', 1.0)

def send_popup(task_title):
	notification.notify(title="Task Reminder",message=task_title,timeout=10 )
	threading.Thread(target=speak_task, args=(task_title,),daemon=True).start)

def setup_scheduler():
	if os.path.exists("Tasks.csv"):
		with open("Tasks.csv", "r", newline="") as taskfile:
			timereader = csv.reader(taskfile)
 			for row in timereader:
			task_title = row[0]
			target_time = row[2]
			schedule.every().day.at(target_time).do(send_popup, task_title=task_title)
def speak_task(task_title):
	engine.say(f"Reminder.{task_tittle}")
	engine.runAndWait()

setup_scheduler()
print("Notification scheduler is running...")
while True:
	schedule.run_pending()
	time.sleep(1)
