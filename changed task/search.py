
import auth
from datetime import datetime
from mysql.connector import Error

def connect_database():
    """
    Use auth.getconnection() so connection settings are centralized in auth.py.
    """
    try:
        conn = auth.getconnection()
        if conn is not None and conn.is_connected():
            print("Database Connected Successfully")
            return conn
    except Error as e:
        print("Database Error:", e)
    return None

def search_tasks(cursor=None):
    """
    Interactive search menu that automatically uses the currently logged-in user.
    If no user is logged in, it returns to caller.
    """
    user_id = auth.get_user_id()
    if user_id is None:
        print("No user logged in. Please login or register first.")
        return

    created_cursor = False
    if cursor is None:
        conn = connect_database()
        if conn is None:
            print("Unable to connect to database.")
            return
        cursor = conn.cursor(dictionary=True)
        created_cursor = True

    try:
        while True:
            print("\n--- Search Tasks ---")
            print("1. Search by Task ID")
            print("2. Search by Date")
            print("3. Search by Status")
            print("4. Search by Tag")
            print("5. Back to Main Menu")

            choice = input("Enter your choice: ").strip()

            # --------------------------------
            # Task ID: search by task id
            # --------------------------------
            if choice == "1":
                while True:
                    task_id = input("Enter Task ID: ").strip()
                    if task_id == "":
                        print("Task ID cannot be empty.")
                        continue
                    if not task_id.isdigit():
                        print("Invalid Task ID. Please enter numbers only.")
                        continue
                    task_id = int(task_id)
                    break

                query = """
                SELECT *
                FROM tasks
                WHERE user_id=%s
                AND id=%s
                ORDER BY deadline
                """
                cursor.execute(query, (user_id, task_id))

            # --------------------------------
            # Date: search by date (task deadline)
            # --------------------------------
            elif choice == "2":
                while True:
                    date = input("Enter Date (YYYY-MM-DD): ").strip()
                    try:
                        datetime.strptime(date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid Date Format. Use YYYY-MM-DD.")

                query = """
                SELECT *
                FROM tasks
                WHERE user_id=%s
                AND DATE(deadline)=%s
                ORDER BY deadline
                """
                cursor.execute(query, (user_id, date))

            # --------------------------------
            # Status: search by status (task status)
            # --------------------------------
            elif choice == "3":
                while True:
                    status = input("Enter Status (pending/completed/overdue): ").strip().lower()
                    if status == "":
                        print("Status cannot be empty.")
                        continue
                    if status.isdigit():
                        print("Invalid Status")
                        continue
                    if status not in ["pending", "completed", "overdue"]:
                        print("Invalid Status.")
                        continue
                    break

                query = """
                SELECT *
                FROM tasks
                WHERE user_id=%s
                AND status=%s
                ORDER BY deadline
                """
                cursor.execute(query, (user_id, status))

            # --------------------------------
            # Tag: search by tag
            # --------------------------------
            elif choice == "4":
                while True:
                    tag = input("Enter Tag: ").strip().lower()
                    if tag == "":
                        print("Tag cannot be empty.")
                        continue
                    if tag.isdigit():
                        print("Invalid Tag.")
                        continue
                    break

                query = """
                SELECT *
                FROM tasks
                WHERE user_id=%s
                AND LOWER(tag)=%s
                ORDER BY deadline
                """
                cursor.execute(query, (user_id, tag))

            # ---------------- Back ----------------
            elif choice == "5":
                print("Returning to Main Menu...")
                return

            else:
                print("Invalid Choice.")
                continue

            result = cursor.fetchall()

            if not result:
                print("\nNo matching tasks found.")
                continue

            print(f"\n{len(result)} Result(s) Found:\n")
            for task in result:
                print("Task ID :", task.get("id"))
                print("Title   :", task.get("title"))
                print("Description :", task.get("description"))
                print("Deadline :", task.get("deadline"))
                print("Priority :", task.get("priority"))
                print("Tag :", task.get("tag"))
                print("Status :", task.get("status"))
                print("----------------------------")

    finally:
        if created_cursor:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

if __name__ == "__main__":
    proceed = auth.login_gate_menu()
    if not proceed:
        print("Exiting.")
    else:
        conn = connect_database()
        if conn:
            cur = conn.cursor(dictionary=True)
            try:
                search_tasks(cur)
            finally:
                cur.close()
                conn.close()
