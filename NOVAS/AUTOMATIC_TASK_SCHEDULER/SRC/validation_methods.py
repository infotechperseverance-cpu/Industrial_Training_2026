from datetime import datetime, date

''' ----------------VALIDATE DATE ,TIME ,CATEGORY,PRIORITY AND TASK NAME----------------- '''

def is_valid_date(date_text):
    try:
        entered_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        current_date = date.today()
        if entered_date < current_date:
            print("Entered date is in the past! Please enter a valid date.")
            return False

        
        return True
    except ValueError:
        return False
    
def is_valid_time(time_of_task):
    try:
        datetime.strptime(time_of_task, "%I:%M %p")
        return True
    except ValueError:
        return False
    
def is_valid_priority(priority_of_task):
    valid_priorities = ["High", "Medium", "Low"]
    return priority_of_task in valid_priorities


def is_valid_task_name(name_of_task):
    if name_of_task.strip() == "":
        print("Task name cannot be empty!")
        return False
    if name_of_task.isnumeric():
        print("Task name cannot be numeric!")
        return False
    if len(name_of_task) > 20:
        print("Task name must be under 20 characters!")
        return False
    return True


def is_valid_category(category_of_task):
    valid_categories = ["Work", "Study", "Personal", "Others"]
    return category_of_task in valid_categories
