from validation_methods import is_valid_category,is_valid_date,is_valid_priority,is_valid_task_name,is_valid_time
import csv
''' ------------USER CAN FILTER TASK BY PRIORITY, DATE, CATEGORY OR STATUS------------ '''
def filter_tasks():
    print("\n--------- Filter Tasks --------\n")
    print("1. Filter tasks by Priority\n")
    print("2. Filter tasks by Task Date\n")
    print("3. Filter tasksby Category\n")
    print("4. Filter tasks by Status\n")
    choice = int(input("Enter choice:\n "))
    
    filtered = []
    
    with open("tasks.csv", "r", newline="") as file:
         reader = csv.DictReader(file)
         tasks_list=list(reader)

    if choice == 1:
        new_priority = input("Enter Priority: ")
        if is_valid_priority(new_priority):
            for t in tasks_list:
                if t["Priority"].lower() == new_priority.lower():
                    filtered.append(t)
    elif choice == 2:
        new_date = input("Enter Date (YYYY-MM-DD): ")
        if is_valid_date(new_date):
            for t in tasks_list:
                if t["Date"] == new_date:
                    filtered.append(t)
    elif choice == 3:
        new_category = input("Enter Category: ")
        if is_valid_category(new_category):
            for t in tasks_list:
                if t["Category"].lower() == new_category.lower():
                    filtered.append(t)
    elif choice == 4:
        new_status = input("Enter Status: ")
        
        
        for t in tasks_list:
            if t["Status"].lower() == new_status.lower():
                filtered.append(t)
    else:
        print("Invalid choice!")
        return

    print("\n--- Filtered Results ---")
    for t in filtered:
        print("Task Name ", t["Task Name"] , " | Date: ", t["Date"], " | Category: ", t["Category"] , " | Status: ", t["Status"])

