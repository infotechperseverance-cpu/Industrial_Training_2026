import csv
import os
from datetime import datetime

def calculate_statistics():
    total_tasks = 0
    completed_tasks = 0
    pending_tasks = 0
    overdue_tasks = 0

    if os.path.exists("tasks.csv"):
        with open('tasks.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                
                total_tasks += 1

                task_DateTime = datetime.strptime(row['Date'] + ' ' + row['Time'], '%Y-%m-%d %I:%M %p')

                if row['Status'] == 'Completed':
                    completed_tasks += 1

                elif row['Status'] == 'Pending':
                    pending_tasks += 1

                if task_DateTime < datetime.now():
                    overdue_tasks += 1
    else:
            print(" tasks.csv file not found")
    
    if os.path.exists("archive.csv"):
        # Read archived (completed) tasks
        with open("archive.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                total_tasks += 1
                completed_tasks += 1

    else:
       # print("archive.csv file not found ")
         pass

    return total_tasks, completed_tasks, pending_tasks, overdue_tasks

def display_statistics():
    total_tasks, completed_tasks, pending_tasks, overdue_tasks = calculate_statistics()
    print("===== Task Statistics =====")
    print(f"Total Tasks     : {total_tasks}")
    print(f"Completed Tasks : {completed_tasks}")
    print(f"Pending Tasks   : {pending_tasks}")
    print(f"Overdue Tasks   : {overdue_tasks}")
    print("===========================")