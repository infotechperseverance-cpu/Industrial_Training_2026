import mysql.connector
from datetime import datetime
import auth
import db

def getconnection():#mysql connecting method
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="task_scheduler_db"
    )
    return connection
def create_task():#creating the task
    user = auth.get_current_user()
    if user is None:                #check if user is loggined or not
        print("Error: Please login first.")
        return

    user_id = user["id"]
    print("\n--- Create Task ---")
    title = input("Task Title: ").strip()
    if title == "":
        print("Title cannot be empty.")
        return
    description = input("Description: ").strip()
    deadline_input = input("Deadline (YYYY-MM-DD HH:MM): ").strip()

    try:
        datetime.strptime(deadline_input, "%Y-%m-%d %H:%M")
        deadline = deadline_input
    except ValueError:
        print("Error: Invalid date/time format.")
        return
    priority = input("Priority (high/medium/low): ").strip().lower()
    if priority not in ["high", "medium", "low"]:
        priority = "medium"

    tag = input("Tag: ").strip()
    if tag == "":
        tag = "General"
    recurring = input("Recurring? (none/daily/weekly/monthly): ").strip().lower()
    if recurring not in ["none", "daily", "weekly", "monthly"]:
        recurring = "none"

    conn = None
    cursor = None
    try:
        conn = getconnection()
        cursor = conn.cursor()
        #insert query with ata value mapping stings
        query = """INSERT INTO tasks (user_id, title, description, tag, deadline, recurring, priority, status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (user_id, title, description, tag, deadline, recurring, priority, "pending"))
        conn.commit()
        print("Task created successfully in MySQL database!")
    except Exception as e:
        print("\n[!] Database Error: Cannot write task data. System disconnected.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def view_edit_delete_menu():
    user = auth.get_current_user()
    if user is None:
        return
    user_id = user["id"]
    user_name = user["name"]
    while True:
        conn = None
        cursor = None
        try:
            conn = getconnection()
            cursor = conn.cursor()

            query = "SELECT id, title, deadline, priority, tag, status FROM tasks WHERE user_id = %s AND status != 'deleted' ORDER BY deadline ASC"
            cursor.execute(query, (user_id,))
            tasks = cursor.fetchall()
            print(f"\n--- Your Tasks ({user_name}) ---")
            if len(tasks) == 0:
                print("No tasks found.")
            else:
             #headers design with fixed column width
                print(f"{'ID':<4} {'Title':<20} {'Deadline':<20} {'Priority':<10} {'Tag':<12} {'Status':<10}")
                print("------------------------------------------------------------------------")
                for task in tasks:
                    print(f"{task[0]:<4} {task[1]:<20} {str(task[2]):<20} {task[3]:<10} {task[4]:<12} {task[5]:<10}")
            print("------------------------------------------------------------------------")
            print("1. View full details of a task")
            print("2. Edit a task")
            print("3. Delete a task")
            print("4. Back to Main Menu")
            print("------------------------------------------------------------------------")

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                task_id = input("Enter Task ID: ").strip()
                if task_id != "": view_task_details(task_id, user_id)
            elif choice == "2":
                task_id = input("Enter Task ID to edit: ").strip()
                if task_id != "": edit_task(task_id, user_id)
            elif choice == "3":
                task_id = input("enter task _id to delete:").strip()
                if task_id == "" or not task_id.isdigit():
                    print("Invalid task id.")
                else:
                    if validate_ownership(task_id, user_id):
                        delete_task(int(task_id), user_id)
                    else:
                        print("id not found")
            elif choice == "4":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("\n[!] Database Error: Tasks view disconnected.")
            break
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

def view_task_details(task_id, user_id):
    conn = None
    cursor = None
    try:
        conn = getconnection()
        cursor = conn.cursor()
        #selecting all details for single specific task belongs to current user
        query = "SELECT title, description, deadline, priority, tag, recurring, status FROM tasks WHERE id = %s AND user_id = %s"
        cursor.execute(query, (task_id, user_id))
        task = cursor.fetchone()
        if task is not None:   #print the details if not none
            print("\n--- Task Details ---")
            print(f"Title       : {task[0]}")
            print(f"Description : {task[1]}")
            print(f"Deadline    : {task[2]}")
            print(f"Priority    : {task[3]}")
            print(f"Tag         : {task[4]}")
            print(f"Recurring   : {task[5]}")
            print(f"Status      : {task[6]}")
        else:
            print("Task not found.")
    except Exception as e:
        print("Error displaying details.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def edit_task(task_id, user_id):
    conn = None
    cursor = None
    try:
        conn = getconnection()
        cursor = conn.cursor()
        # query for checking the task is exist and active
        query = "SELECT title, deadline, priority, tag FROM tasks WHERE id = %s AND user_id = %s AND status != 'deleted'"
        cursor.execute(query, (task_id, user_id))
        task = cursor.fetchone()

        if task is None:
            print("Task not found.")
            return
        print("Leave blank to keep old values.") # taking input while showing old values
        new_title = input(f"New Title [{task[0]}]: ").strip()
        new_deadline = input(f"New Deadline [{task[1]}]: ").strip()
        new_priority = input(f"New Priority [{task[2]}]: ").strip().lower()
        new_tag = input(f"New Tag [{task[3]}]: ").strip()
        # if user enter nothing restore the old values
        if new_title == "": new_title = task[0]
        if new_deadline == "":
            new_deadline = task[1]
        else:
            try:
                datetime.strptime(new_deadline, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid date format. Aborted.")
                return
        if new_priority == "": new_priority = task[2]
        if new_tag == "": new_tag = task[3]
        # query to save updated values
        update_query = "UPDATE tasks SET title = %s, deadline = %s, priority = %s, tag = %s WHERE id = %s AND user_id = %s"
        cursor.execute(update_query, (new_title, new_deadline, new_priority, new_tag, task_id, user_id))
        conn.commit()
        print("Task updated successfully.")
    except Exception as e:
        print("Error updating task data.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_task(task_id, user_id):# deleting the task
    conn = db.getconnection()
    cursor = conn.cursor()

    try:
        copy = "INSERT IGNORE INTO recycle_bin SELECT * FROM tasks WHERE id=%s AND user_id=%s"
        cursor.execute(copy, (task_id, user_id))

        query = "DELETE FROM tasks WHERE id=%s AND user_id=%s"
        cursor.execute(query, (task_id, user_id))
        conn.commit()
        print("task deleted successfully")
    except Exception as e:
        print("Error deleting task data.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
def validate_ownership(task_id, user_id):# validate ownership to protect unauthorized read
    conn = None
    cursor = None
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks WHERE id=%s AND user_id=%s", (task_id, user_id))
        row = cursor.fetchone()
        return row is not None   # return true if task belongs to user
    except Exception:
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
