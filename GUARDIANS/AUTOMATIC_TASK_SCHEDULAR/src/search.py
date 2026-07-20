import mysql.connector
from mysql.connector import Error

def connect_database():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Admin@123",
            database="task_scheduler"
        )

        if connection.is_connected():
            print("Database Connected Successfully")
            return connection

    except Error as e:
        print("Database Error:", e)
        return None

from datetime import datetime

def search_tasks(cursor, user_id):

    while True:

        print("\n--- Search Tasks ---")
        print("1. Search by Task ID")
        print("2. Search by Date")
        print("3. Search by Status")
        print("4. Search by Tag")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        
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
        #date:search by date(task deadline)
        #---------------------------------
        elif choice == "2":
            while True:
                date = input("Enter Date (YYYY-MM-DD): ")

                


                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid Date Format.")
                
                

            query = """
            SELECT *
            FROM tasks
            WHERE user_id=%s
            AND DATE(deadline)=%s
            ORDER BY deadline
            """

            cursor.execute(query, (user_id, date))

        # --------------------------------
        #status:search by status(task status)
        #---------------------------------
        elif choice == "3":
            while True:
                status = (input("Enter Status (pending/completed/overdue): ")).strip().lower()
                if status == "":
                    print("status cannot be empty.")
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

        if len(result) == 0:
            print("\nNo matching tasks found.")
            continue

        else:

            print(f"\n{len(result)} Result(s) Found:\n")

            for task in result:

                print("Task ID :", task["id"])
                print("Title :", task["title"])
                print("Description :", task["description"])
                print("Deadline :", task["deadline"])
                print("Priority :", task["priority"])
                print("Tag :", task["tag"])
                print("Status :", task["status"])
                print("----------------------------")
                continue

if __name__ == "__main__":

    connection = connect_database()

    if connection:

        cursor = connection.cursor(dictionary=True)

        while True:

            try:
                user_id = int(input("Enter User ID: "))
            except ValueError:
                print("Invalid User ID. Please enter numbers only.")
                continue

            cursor.execute("SELECT id FROM users WHERE id=%s", (user_id,))
            user = cursor.fetchone()

            if user:
                break

            print("User ID not found. Please enter a Registered User ID")

        search_tasks(cursor, user_id)

        cursor.close()
        connection.close()