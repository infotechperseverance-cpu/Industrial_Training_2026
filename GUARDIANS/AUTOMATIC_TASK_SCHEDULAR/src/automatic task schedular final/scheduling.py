import mysql.connector
from datetime import datetime
import db

print("Welcome to the Task Scheduler!")


def schedule_task(user_id):
    try:
        # Implementation for scheduling a task

        title = input("Enter the title of the task:")
        description = input("Enter the description of the task:")
        tag = input("Enter the tag for the task:")
        date = input("Enter the due date of the task (YYYY-MM-DD): ")
        time = input("Enter the due time of the task (HH:MM:SS): ")
        deadline = date + " " + time
        datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")
        priority = input("Enter the priority of the task (High, Medium, Low): ").lower()
        if priority not in ["high", "medium", "low"]:
            print("Invalid priority.")
            return
        recurring = input("Is this task recurring? (none/daily/weekly/monthly): ").lower()
        if recurring not in ["none", "daily", "weekly", "monthly"]:
            print("Invalid recurring option.")
            return
        l = [user_id, title, description, tag, deadline, recurring, priority, 'pending']
        db.insert_task(l)

    except ValueError:
        print("Invalid date or time format.")

    except Exception as e:
        print("Error:", e)


def modify_task(user_id):
    try:
        db.show_tasks(user_id)
        task_id = input("enter task _id:")
        task_title = input("Enter the new title of the task: ")
        task_description = input("Enter the new description of the task: ")
        tag = input("enter tag to update:")
        date = input("Enter the new due date of the task (YYYY-MM-DD): ")
        time = input("Enter the new due time of the task (HH:MM:SS): ")
        dateline = date + " " + time
        datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")
        priority = input("Enter the new priority of the task (High, Medium, Low): ").lower()
        if priority not in ["high", "medium", "low"]:
            print("invalid priority")
            return
        status = input("Enter the new status of the task (pending/completed): ").lower()
        if status not in ["pending", "completed"]:
            print("invaild status")
            return
        recurring = input("Is this task recurring? (none/daily/weekly/monthly): ").lower()
        if recurring not in ["none", "daily", "weekly", "monthly"]:
            print("invaild recurring")
            return

        update_query = "UPDATE tasks SET title=%s, description=%s, tag=%s, deadline=%s, priority=%s, status=%s, recurring=%s WHERE id=%s AND user_id=%s"
        db.cursor.execute(update_query, (task_title, task_description, tag, dateline, priority, status, recurring, task_id, user_id))
        db.conn.commit()
        print("Task updated successfully.")
    except ValueError:
        print("invaild date or time format")
    except Exception as e:
        print("error:", e)


def delete_task(user_id):
    db.show_tasks(user_id)
    task_id = input("Enter the task ID to delete: ")
    db.delete_task(task_id, user_id)


user_id = int(input("enter user_id:"))
while True:
    match input(
        "========== ENTER CHOISE ========== \n 1. Schedule a task\n 2. View tasks\n 3. Modify task\n 4. Delete task\n 5. Restore tasks\n 6. Exit \n choise ?: "):
        case "1":

            schedule_task(user_id)
        case "2":

            db.show_tasks(user_id)
        case "3":

            modify_task(user_id)
        case "4":

            delete_task(user_id)
        case "5":

            task_id = input("Enter the task ID to restore: ")
            db.restore_task(task_id, user_id)
        case "6":
            print("Exiting the Task Scheduler. Goodbye!")
            break
        case _:
            print("Invalid choice. Please try again.")