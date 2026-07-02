from datetime import datetime, date
from validation_methods import is_valid_category,is_valid_date,is_valid_priority,is_valid_task_name,is_valid_time
from record_due_tasks import record_completion,record_creation
import csv
''' ---------USER CAN UPDATE THE TASK DETAILS--------'''

def update_task_details():
    with open("tasks.csv", "r", newline="") as file:
         reader = csv.DictReader(file)
         tasks_list=list(reader)
    print("\n--- Update Task Details ---")
    id = input("Enter the task id : ")
    for t in tasks_list:
        if t["Task ID"] == id:
            print("Task found !!\nwhat update do yo want to make : ")
            print("1. Update task name\n")
            print("2. Update date\n")
            print("3. Update time\n")
            print("4. Update priority\n")
            print("5. Update status\n")
            print("6. Update category\n")

            choice = int(input("Enter choice: "))
            
            if choice == 1:
                new_task_name = input("Enter new task name: ")
                if is_valid_task_name(new_task_name):
                    t["Task Name"] = new_task_name
                    print("Task name is updated!")
                else:
                    print("Invalid task name! Please enter a valid task name.")
                    return

    
            elif choice == 2:
                new_date = input("Enter new date (YYYY-MM-DD): ")
                if is_valid_date(new_date):
                    t["Date"] = new_date
                    print("Date is updated!")
                else:
                    print("Invalid date format! Please enter a valid date.")
            elif choice == 3:
                new_time = input("Enter new time (HH:MM): ")
                if is_valid_time(new_time):
                    t["Time"] = new_time
                    print("Time is updated!")
                else:
                    print("Invalid time format! Please enter a valid time in HH:MM format.")
                    return
            elif choice == 4:
                new_priority = input("Enter new priority (High/Medium/Low): ")
                if is_valid_priority(new_priority):
                    t["Priority"] = new_priority
                    print("Priority is updated!")
                else:
                    print("Invalid priority! Choice must be High, Medium, or Low .")
                    return
            elif choice == 5:
                new_status = input("Enter new status: ")
                if new_status.lower() == "completed":
                    record_completion(t)
                else:
                    t["Status"] = new_status
                print("Status is updated!")
            elif choice == 6:
                new_category = input("Enter new category: ")
                if is_valid_category(new_category):
                    t["Category"]= new_category
                    print("Category is updated!")
                else:
                    print("Invalid category! Choice can be Work, Study, Personal, or Other.")
                    return
            else:
                print("Invalid choice!")
