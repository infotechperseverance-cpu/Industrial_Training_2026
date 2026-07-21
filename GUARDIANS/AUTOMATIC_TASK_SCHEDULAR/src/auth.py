import mysql.connector
import notification1
from notification1 import check_overdue_tasks

# global variable for login details
current_user = None

def getconnection(): # mysql connection module
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="task_scheduler_db"
    )
    return connection
def register_user():
    print("\n--- New User Registration ---")
    name = input("Full Name: ").strip()
    email = input("Email: ").strip()
    username = input("Choose a Username: ").strip()
    password = input("Choose a Password: ")
    confirm_password = input("Confirm Password: ")

    # validations
    if name == "" or email == "" or username == "" or password == "":
        print("Error: All fields are mandatory.")
        return

    if " " in username:
        print("Error: Username cannot contain spaces.")
        return
    if "@" not in email or "." not in email:
        print("Error: Invalid email format.")
        return
    if len(password) < 6:
        print("Error: Password must be at least 6 characters long.")
        return
    if password != confirm_password:
        print("Passwords do not match.")
        return

    conn = None
    cursor = None
    try:
        conn = getconnection()
        cursor = conn.cursor()

        check_user_query = "SELECT id FROM users WHERE username = %s" # verifying the username
        cursor.execute(check_user_query, (username,))
        if cursor.fetchone() is not None:
            print("This username is already taken.")
            return
        #query for stroring the data 
        insert_query = "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (name, email, username, password))
        conn.commit()

        print(f"Account created successfully for {username}!")

        cursor.execute("SELECT id, name FROM users WHERE username = %s", (username,))
        new_user = cursor.fetchone()
        global current_user
        current_user = {"id": new_user[0], "name": new_user[1], "username": username}
    except Exception as e:
        print("\n[!] Connection Error: Database is not responding.")
        print("Please check if MySQL Server is running or password matches your system configuration.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def login_user():
    print("\n--- Existing User Login ---")
    username = input("Username: ").strip()
    password = input("Password: ")

    if username == "" or password == "":
        print("Error: Fields cannot be empty.")
        return

    conn = None
    cursor = None
    try:
        conn = getconnection()
        cursor = conn.cursor()
        #comparing login details
        query = "SELECT id, name, password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result is not None:
            db_id, db_name, db_password = result
            if password == db_password:
                print(f"Login successful! Welcome back, {db_name}.")
                global current_user
                current_user = {"id": db_id, "name": db_name, "username": username}

                check_overdue_tasks(username)#check status on startup
            else:
                print("Incorrect username or password.")
        else:
            print("Incorrect username or password.")
    except Exception as e:
        print("\n[!] Connection Error: Database is not responding.")
        print("Please check if MySQL Server is running or password matches your system configuration.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def logout_user():
    global current_user
    if current_user is None:
        print("You are not logged in.")
        return
    print("Logged out successfully.")
    current_user = None
def get_current_user():#getting the current user 
    global current_user
    return current_user
def is_logged_in():#checking the login
    global current_user
    return current_user is not None
def login_gate_menu():
    while True:
        if is_logged_in():
            return True
        print("=============================")
        print("AUTOMATIC TASK SCHEDULER")
        print("=============================")
        print("1. New User (Register)")
        print("2. Existing User (Login)")
        print("3. Exit")
        print("=============================")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Goodbye!")
            return False
        else:
            print("Invalid choice. Enter 1, 2, or 3.")
def get_username():
    #returns the username of current user
    global current_user
    if current_user is not None:
        return current_user["username"]
    else:
        return None
def get_user_id():
    # returns the user_id of current user
    global current_user
    if current_user is not None:
        return current_user["id"]
    else:
        return None
