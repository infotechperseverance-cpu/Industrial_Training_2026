import mysql.connector
from mysql.connector import Error
from datetime import datetime
import auth

def get_connection():
    return mysql.connector.connect( host="localhost", user="root", password="WJ28@krhps", database="task_scheduler_db"  )

def get_valid_user_id():
    while True:
        try:
            user_id = int(input("Enter User ID: "))
            if user_id <= 0:
                print("User ID must be a positive number.")
                continue
            return user_id
        except ValueError:
            print("Invalid input! Please enter a valid numeric User ID.")

def print_tasks(tasks, label):
    print(f"\n========== {label} TASK(S) ==========")
    if len(tasks) == 0:
        print(f"No {label.lower()} task found for this user.")
    else:
        for task in tasks:
            print("\nTask ID      :", task[0])
            print("Title        :", task[1])
            print("Description  :", task[2])
            print("Priority     :", task[3])
            print("Deadline     :", task[4])
            print("User ID      :", task[5])

def view_completed_tasks(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT id, title, description, priority,
               deadline, user_id
        FROM tasks
        WHERE status = 'complete' AND user_id = %s
    """

    cursor.execute(query, (user_id,))
    tasks = cursor.fetchall()
    print_tasks(tasks, "COMPLETED")

    cursor.close()
    connection.close()

def view_pending_tasks(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT id, title, description, priority,
               deadline, user_id
        FROM tasks
        WHERE status = 'pending' AND user_id = %s
    """

    cursor.execute(query, (user_id,))
    tasks = cursor.fetchall()
    print_tasks(tasks, "PENDING")

    cursor.close()
    connection.close()

def view_missed_tasks(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT id, title, description, priority,
               deadline, user_id
        FROM tasks
        WHERE status = 'overdue' AND user_id = %s
    """

    cursor.execute(query, (user_id,))
    tasks = cursor.fetchall()
    print_tasks(tasks, "MISSED")

    cursor.close()
    connection.close()

def generate_summary_report(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = %s", (user_id,))
    total_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'complete' AND user_id = %s", (user_id,))
    completed_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'overdue' AND user_id = %s", (user_id,))
    missed_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending' AND user_id = %s", (user_id,))
    pending_tasks = cursor.fetchone()[0]

    print("\n========== SUMMARY REPORT ==========")
    print("Report Generated At :", datetime.now())
    print("------------------------------------")
    print("User ID            :", user_id)
    print("Total Tasks        :", total_tasks)
    print("Completed Tasks    :", completed_tasks)
    print("Missed Tasks       :", missed_tasks)
    print("Pending Tasks      :", pending_tasks)

    cursor.close()
    connection.close()

#main
if __name__ == "__main__":

    proceed = auth.login_gate_menu()
    if not proceed:
        print("Exiting.")
    else:
        user_id = auth.get_user_id()
        if user_id is None:
            user_id = get_valid_user_id()

        while True:
            print("\n========== REPORTS & HISTORY ==========")
            print("1. View Completed Task")
            print("2. View Missed Task")
            print("3. View Pending Task")
            print("4. Generate Summary Report")
            print("5. Back to main menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                view_completed_tasks(user_id)
            elif choice == "2":
                view_missed_tasks(user_id)
            elif choice == "3":
                view_pending_tasks(user_id)
            elif choice == "4":
                generate_summary_report(user_id)
            elif choice == "5":
                print("Returning to main menu....")
                break
            else:
                print("Invalid choice. Please try again.")