import os
import csv
import time
from datetime import datetime
import schedule
from plyer import notification
def send_popup(task_title):
	notification.notify(title="Task Reminder",message=task_title,timeout=10 )

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
