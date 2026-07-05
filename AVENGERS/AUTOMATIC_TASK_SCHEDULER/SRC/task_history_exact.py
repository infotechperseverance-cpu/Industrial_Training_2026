import csv
import os 
from datetime import datetime

history_file = 'task_history.csv'

if not os.path.exists(history_file):
    with open(history_file, "w", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow(["Task_ID", "Task_Name", "Action", "Status", "Date_Time"])


# Add this code in add_task() in task management module 

    with open(history_file, "a", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow([task_ID, task_name, "Created", status,
                         datetime.now().strftime("%d/%m/%Y %I:%M %p")])


# Add this code in update_task() in task management module 

    with open(history_file, "a", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow([task_ID, task_name, "Updated", status,
                         datetime.now().strftime("%d/%m/%Y %I:%M %p")])


# Add this code in delete_task() in task management module 

    with open(history_file, "a", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow([task_ID, task_name, "Deleted", status,
                         datetime.now().strftime("%d/%m/%Y %I:%M %p")])


# Add this code in undo_delete in task management module 

    with open(history_file, "a", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow([task_ID, task_name, "Undo Delete", status,
                         datetime.now().strftime("%d/%m/%Y %I:%M %p")])


# Add this code in recurring_task() in task_management module 

    with open(history_file, "a", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow([task_ID, task_name, "Recurring", status,
                         datetime.now().strftime("%d/%m/%Y %I:%M %p")])

def view_history():

    try:
        with open(history_file, "r", newline="") as hf:
            reader = csv.reader(hf)

            print("--------- TASK HISTORY ------------\n")
            for row in reader:
                print(*row,sep="\t")

    except FileNotFoundError:
        print("No task history found.")

view_history()
