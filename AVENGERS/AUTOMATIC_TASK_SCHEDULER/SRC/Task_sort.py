import csv
import os
from datetime import datetime
tasklist = []
# Read Tasks.csv
if os.path.exists("Tasks.csv"):
   with open("Tasks.csv", newline="") as taskfile:
     taskreader = csv.reader(taskfile)

   for row in taskreader:
     tasklist.append(row)

def sort_task_by_status():
   with open("completedTasks.csv", "w", newline="") as completefile, \
      open("pendingTasks.csv", "w", newline="") as pendingfile, \
      open("failedTasks.csv", "w", newline="") as failedfile:
      completewrite = csv.writer(completefile)
      pendingwrite = csv.writer(pendingfile)
      failedwrite = csv.writer(failedfile)

      for task in tasklist:
         status = task[3].strip().lower()
         if status == "completed":
           completewrite.writerow(task)
         elif status == "pending":
           pendingwrite.writerow(task)
         else:
           failedwrite.writerow(task)

def prioritize():
   tasklist.sort(key=lambda task: datetime.strptime(task[1] + " " + task[2],"%d-%m-%Y %H:%M"))
   with open("prioritized.csv", "w", newline="") as priorityfile:
      prioritywrite = csv.writer(priorityfile)
      for task in tasklist:
        prioritywrite.writerow(task)

sort_task_by_status()
prioritize()