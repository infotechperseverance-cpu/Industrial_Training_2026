from db import get_connection
from logger import write_log


# ==========================================
# USER MANAGEMENT FUNCTIONS
# ==========================================

def add_user(username, password, role):
    conn, cursor = get_connection()

    try:
        cursor.execute("""
            INSERT INTO users(username, password, role)
            VALUES(?,?,?)
        """, (username, password, role))

        conn.commit()
        print("\nUser Added Successfully.")
        write_log("Add User", "Success")

    except Exception as e:
        print("\nError:", e)
        write_log("Add User", "Failure", str(e))

    finally:
        conn.close()


def login(username, password):
    conn, cursor = get_connection()

    cursor.execute("""
        SELECT user_id, username, role
        FROM users
        WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()

    conn.close()

    if user:
        print(f"\nWelcome {user[1]} ({user[2]})")
        write_log("Login", "Success")
        return user

    else:
        print("\nInvalid Username or Password")
        write_log("Login", "Failure", "Invalid Credentials")
        return None


def show_users():
    conn, cursor = get_connection()

    cursor.execute("""
        SELECT user_id,
               username,
               role
        FROM users
        ORDER BY user_id
    """)

    users = cursor.fetchall()

    print("\n========== USERS ==========")

    if len(users) == 0:
        print("No users found.")

    else:
        for user in users:
            print(f"""
User ID : {user[0]}
Username: {user[1]}
Role    : {user[2]}
-----------------------------
""")

    conn.close()


def update_user(user_id):

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE user_id=?
    """, (user_id,))

    user = cursor.fetchone()

    if user is None:
        print("User not found.")
        conn.close()
        return

    print("\nLeave blank if you don't want to change the value.\n")

    username = input("New Username : ")
    password = input("New Password : ")
    role = input("Role(Admin/User) : ")

    if username == "":
        username = user[1]

    if password == "":
        password = user[2]

    if role == "":
        role = user[3]

    try:

        cursor.execute("""
            UPDATE users
            SET username=?,
                password=?,
                role=?
            WHERE user_id=?
        """, (username, password, role, user_id))

        conn.commit()

        print("\nUser Updated Successfully.")
        write_log("Update User", "Success")

    except Exception as e:

        print(e)
        write_log("Update User", "Failure", str(e))

    finally:

        conn.close()


def delete_user(user_id):

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE user_id=?
    """, (user_id,))

    if cursor.fetchone() is None:

        print("User not found.")
        conn.close()
        return

    try:

        cursor.execute("""
            DELETE FROM users
            WHERE user_id=?
        """, (user_id,))

        conn.commit()

        print("User Deleted Successfully.")
        write_log("Delete User", "Success")

    except Exception as e:

        print(e)
        write_log("Delete User", "Failure", str(e))

    finally:

        conn.close()


def search_user(user_id):

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT user_id,
               username,
               role
        FROM users
        WHERE user_id=?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    if user:

        print("\n========== USER DETAILS ==========")

        print("User ID :", user[0])
        print("Username:", user[1])
        print("Role    :", user[2])

    else:

        print("User not found.")

# ==========================================
# TASK MANAGEMENT
# ==========================================

def assign_task(user_id, task_name, assigned_date, due_date):
    conn, cursor = get_connection()

    try:
        cursor.execute("""
            INSERT INTO tasks(user_id, task_name, assigned_date, due_date)
            VALUES (?, ?, ?, ?)
        """, (user_id, task_name, assigned_date, due_date))

        conn.commit()

        print("\nTask Assigned Successfully.")
        write_log("Assign Task", "Success")

    except Exception as e:
        print("Error:", e)
        write_log("Assign Task", "Failure", str(e))

    finally:
        conn.close()


def show_all_tasks():

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT task_id,
               user_id,
               task_name,
               status,
               assigned_date,
               due_date
        FROM tasks
        ORDER BY task_id
    """)

    tasks = cursor.fetchall()

    print("\n============= ALL TASKS =============")

    if len(tasks) == 0:
        print("No Tasks Available.")

    else:

        for task in tasks:

            print(f"""
Task ID        : {task[0]}
User ID        : {task[1]}
Task Name      : {task[2]}
Status         : {task[3]}
Assigned Date  : {task[4]}
Due Date       : {task[5]}
----------------------------------------
""")

    conn.close()


def show_my_tasks(user_id):

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT task_id,
               task_name,
               status,
               assigned_date,
               due_date
        FROM tasks
        WHERE user_id=?
        ORDER BY task_id
    """, (user_id,))

    tasks = cursor.fetchall()

    print("\n============= MY TASKS =============")

    if len(tasks) == 0:

        print("No Tasks Assigned.")

    else:

        for task in tasks:

            print(f"""
Task ID        : {task[0]}
Task Name      : {task[1]}
Status         : {task[2]}
Assigned Date  : {task[3]}
Due Date       : {task[4]}
----------------------------------------
""")

    conn.close()


def update_task_status(task_id, status):

    conn, cursor = get_connection()

    try:

        cursor.execute("""
            UPDATE tasks
            SET status=?
            WHERE task_id=?
        """, (status, task_id))

        conn.commit()

        print("\nTask Status Updated.")
        write_log("Update Task Status", "Success")

    except Exception as e:

        print(e)
        write_log("Update Task Status", "Failure", str(e))

    finally:

        conn.close()


# ==========================================
# NOTIFICATION MANAGEMENT
# ==========================================

def send_notification(user_id, message):

    conn, cursor = get_connection()

    try:

        cursor.execute("""
            INSERT INTO notifications(user_id, message)
            VALUES (?, ?)
        """, (user_id, message))

        conn.commit()

        print("Notification Sent.")
        write_log("Send Notification", "Success")

    except Exception as e:

        print(e)
        write_log("Send Notification", "Failure", str(e))

    finally:

        conn.close()


def show_notifications(user_id):

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT notification_id,
               message,
               sent_time
        FROM notifications
        WHERE user_id=?
        ORDER BY notification_id DESC
    """, (user_id,))

    notifications = cursor.fetchall()

    print("\n========== MY NOTIFICATIONS ==========")

    if len(notifications) == 0:

        print("No Notifications.")

    else:

        for notification in notifications:

            print(f"""
Notification ID : {notification[0]}
Message         : {notification[1]}
Sent Time       : {notification[2]}
----------------------------------------
""")

# ==========================================
# ADMIN MENU
# ==========================================

def admin_menu():

    while True:

        print("\n========== ADMIN MENU ==========")
        print("1. Add User")
        print("2. View Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Search User")
        print("6. Assign Task")
        print("7. View All Tasks")
        print("8. Update Task Status")
        print("9. Send Notification")
        print("10. Logout")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            username = input("Username : ")
            password = input("Password : ")
            role = input("Role (Admin/User) : ")

            if role not in ("Admin", "User"):
                print("Invalid role.")
                continue

            add_user(username, password, role)

        elif choice == "2":

            show_users()

        elif choice == "3":

            user_id = int(input("User ID : "))
            update_user(user_id)

        elif choice == "4":

            user_id = int(input("User ID : "))
            delete_user(user_id)

        elif choice == "5":

            user_id = int(input("User ID : "))
            search_user(user_id)

        elif choice == "6":

            user_id = int(input("Assign To User ID : "))
            task = input("Task Name : ")
            assigned = input("Assigned Date (YYYY-MM-DD): ")
            due = input("Due Date (YYYY-MM-DD): ")

            assign_task(user_id, task, assigned, due)

        elif choice == "7":

            show_all_tasks()

        elif choice == "8":

            task_id = int(input("Task ID : "))
            status = input("Status : ")

            update_task_status(task_id, status)

        elif choice == "9":

            user_id = int(input("User ID : "))
            message = input("Message : ")

            send_notification(user_id, message)

        elif choice == "10":

            print("\nLogged Out Successfully.")
            break

        else:

            print("Invalid Choice.")


# ==========================================
# USER MENU
# ==========================================

def user_menu(user_id):

    while True:

        print("\n========== USER MENU ==========")
        print("1. View My Tasks")
        print("2. Update My Task Status")
        print("3. View My Notifications")
        print("4. Logout")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            show_my_tasks(user_id)

        elif choice == "2":

            show_my_tasks(user_id)

            task_id = int(input("\nEnter Task ID : "))
            status = input("Enter New Status : ")

            conn, cursor = get_connection()

            cursor.execute("""
                SELECT *
                FROM tasks
                WHERE task_id=? AND user_id=?
            """, (task_id, user_id))

            task = cursor.fetchone()

            if task:

                cursor.execute("""
                    UPDATE tasks
                    SET status=?
                    WHERE task_id=?
                """, (status, task_id))

                conn.commit()

                print("\nTask Status Updated Successfully.")
                write_log("Update Own Task", "Success")

            else:

                print("\nYou can only update your own tasks.")
                write_log(
                    "Update Own Task",
                    "Failure",
                    "Unauthorized Task Update Attempt"
                )

            conn.close()

        elif choice == "3":

            show_notifications(user_id)

        elif choice == "4":

            print("\nLogged Out Successfully.")
            break

        else:

            print("Invalid Choice.")

# ==========================================
# LOGIN SYSTEM
# ==========================================

def start():

    print("\n========== PROCESS AUTOMATION ==========")

    username = input("Username : ")
    password = input("Password : ")

    user = login(username, password)

    if user is None:
        return

    user_id = user[0]
    role = user[2]

    if role == "Admin":
        admin_menu()

    else:
        user_menu(user_id)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    while True:

        print("\n========== MAIN MENU ==========")
        print("1. Login")
        print("2. Exit")

        choice = input("Enter Choice : ")

        if choice == "1":

            start()

        elif choice == "2":

            print("\nThank You!")
            break

        else:

            print("Invalid Choice.")