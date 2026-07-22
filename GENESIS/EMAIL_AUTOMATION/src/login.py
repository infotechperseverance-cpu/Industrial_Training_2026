"""
==============================================================================
                            LOGIN MODULE
==============================================================================

Project Name : Email Automation System
Module Name  : login.py

Description:
This module is responsible for

1. User Registration
2. User Login
3. MySQL Database Connection
4. Gmail Validation
5. Password Masking

==============================================================================
"""

import re
import sys
import msvcrt
import mysql.connector
from mysql.connector import Error

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

HOST = "localhost"
USER = "root"
PASSWORD = "root123"      # Change according to your MySQL password
DATABASE = "email_automation"


# ============================================================================
# FUNCTION : create_database()
# PURPOSE  : Creates the database if it does not exist.
# ============================================================================

def create_database():

    connection = None
    cursor = None

    try:

        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )

        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DATABASE}"
        )

        connection.commit()

    except Error as e:

        print("\nDatabase Creation Error")
        print(e)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================================
# FUNCTION : db_connection()
# PURPOSE  : Connects to MySQL database.
# ============================================================================

def db_connection():

    create_database()

    try:

        connection = mysql.connector.connect(

            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE

        )

        return connection

    except Error as e:

        print("\n======================================")
        print("DATABASE CONNECTION FAILED")
        print("======================================")

        print(e)

        print("\nPossible Reasons")
        print("----------------------------")
        print("1. MySQL Service is not running.")
        print("2. Wrong Username.")
        print("3. Wrong Password.")
        print("4. Database does not exist.")

        return None


# ============================================================================
# FUNCTION : create_table()
# PURPOSE  : Creates users table.
# ============================================================================

def create_table():

    conn = db_connection()

    if conn is None:
        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        query = """
        CREATE TABLE IF NOT EXISTS users
        (
            id INT AUTO_INCREMENT PRIMARY KEY,

            user_id VARCHAR(150)
            UNIQUE
            NOT NULL,

            password VARCHAR(255)
            NOT NULL
        )
        """

        cursor.execute(query)

        conn.commit()

    except Error as e:

        print("\nTable Creation Error")
        print(e)

    finally:

        if cursor:
            cursor.close()

        conn.close()


# ============================================================================
# FUNCTION : check_email()
# PURPOSE  : Checks whether Gmail ID is valid.
# ============================================================================

def check_email(email):

    pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'

    return bool(re.fullmatch(pattern, email))


# ============================================================================
# FUNCTION : get_password()
# PURPOSE  : Reads password using '*' symbols.
# ============================================================================

def get_password(prompt="Enter Password : "):

    print(prompt, end="", flush=True)

    password = ""

    while True:

        ch = msvcrt.getch()

        # ENTER KEY

        if ch in (b'\r', b'\n'):

            print()

            break

        # BACKSPACE

        elif ch == b'\x08':

            if len(password) > 0:

                password = password[:-1]

                sys.stdout.write("\b \b")

                sys.stdout.flush()

        else:

            try:

                character = ch.decode("utf-8")

                password += character

                sys.stdout.write("*")

                sys.stdout.flush()

            except:

                pass

    return password

# ============================================================================
# FUNCTION : register()
# PURPOSE  : Registers a new Gmail account in the database.
# INPUT    : None
# OUTPUT   : Stores Gmail ID and App Password in MySQL.
# ============================================================================

def register():

    # Create table if it does not exist
    create_table()

    print("\n======================================")
    print("         USER REGISTRATION")
    print("======================================")

    # ---------------------------------------------------------
    # Gmail Validation
    # ---------------------------------------------------------

    while True:

        email = input("Enter Gmail ID : ").strip()

        if email == "":

            print("\nEmail cannot be empty.")

            continue

        if not check_email(email):

            print("\nPlease enter a valid Gmail ID.")
            print("Example : example@gmail.com")

            continue

        break

    # ---------------------------------------------------------
    # Gmail App Password Validation
    # ---------------------------------------------------------

    while True:

        password = get_password("Enter Gmail App Password : ")

        # Remove spaces (Google sometimes displays it grouped)
        password = password.replace(" ", "")

        if password == "":

            print("\nPassword cannot be empty.")

            continue

        # Gmail App Password should be 16 characters
        if len(password) != 16:

            print("\nInvalid Gmail App Password.")
            print("App Password must contain exactly 16 characters.")

            continue

        break

    # ---------------------------------------------------------
    # Database Connection
    # ---------------------------------------------------------

    conn = db_connection()

    if conn is None:

        return False

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        # -----------------------------------------------------
        # Check whether email already exists
        # -----------------------------------------------------

        cursor.execute(

            "SELECT id FROM users WHERE user_id=%s",

            (email,)
        )

        record = cursor.fetchone()

        if record:

            print("\n======================================")
            print("ACCOUNT ALREADY EXISTS")
            print("======================================")
            print("This Gmail ID is already registered.")

            return False

        # -----------------------------------------------------
        # Insert New User
        # -----------------------------------------------------

        cursor.execute(

            """
            INSERT INTO users(user_id, password)
            VALUES(%s, %s)
            """,

            (email, password)
        )

        conn.commit()

        print("\n======================================")
        print("REGISTRATION SUCCESSFUL")
        print("======================================")
        print("Your account has been created successfully.")
        print("You can now login using your Gmail ID.")

        return True

    except Error as e:

        print("\nRegistration Error")
        print(e)

        conn.rollback()

        return False

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# ============================================================================
# FUNCTION : login()
# PURPOSE  : Authenticates the user using Gmail ID and App Password.
# INPUT    : None
# OUTPUT   : Returns (email, password) after successful login.
# ============================================================================

def login():

    # Create table if it does not exist
    create_table()

    print("\n======================================")
    print("            USER LOGIN")
    print("======================================")

    # ---------------------------------------------------------
    # Enter Gmail ID
    # ---------------------------------------------------------

    email = input("Enter Gmail ID : ").strip()

    if email == "":

        print("\nEmail cannot be empty.")

        return None, None

    if not check_email(email):

        print("\nInvalid Gmail ID.")
        print("Please enter a valid Gmail address.")

        return None, None

    # ---------------------------------------------------------
    # Connect Database
    # ---------------------------------------------------------

    conn = db_connection()

    if conn is None:

        return None, None

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        # -----------------------------------------------------
        # Check whether email exists
        # -----------------------------------------------------

        cursor.execute(

            "SELECT password FROM users WHERE user_id=%s",

            (email,)
        )

        record = cursor.fetchone()

        # -----------------------------------------------------
        # User not registered
        # -----------------------------------------------------

        if record is None:

            print("\n======================================")
            print("USER NOT REGISTERED")
            print("======================================")
            print("This Gmail ID is not registered.")
            print("Please register first.")

            choice = input("\nDo you want to register? (Y/N): ").strip().upper()

            if choice == "Y":

                register()

            return None, None

        # -----------------------------------------------------
        # Enter Password
        # -----------------------------------------------------

        password = get_password("Enter Gmail App Password : ")

        password = password.replace(" ", "")

        if password == "":

            print("\nPassword cannot be empty.")

            return None, None

        # -----------------------------------------------------
        # Verify Password
        # -----------------------------------------------------

        stored_password = record[0]

        if password != stored_password:

            print("\n======================================")
            print("LOGIN FAILED")
            print("======================================")
            print("Incorrect App Password.")

            return None, None

        # -----------------------------------------------------
        # Login Successful
        # -----------------------------------------------------

        print("\n======================================")
        print("        LOGIN SUCCESSFUL")
        print("======================================")
        print("Welcome,", email)

        return email, password

    except Error as e:

        print("\nLogin Error")
        print(e)

        return None, None

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# ============================================================================
# MAIN PROGRAM
# PURPOSE : Demonstrates Registration and Login Module
# ============================================================================

if __name__ == "__main__":

    while True:

        print("\n======================================")
        print("       EMAIL AUTOMATION SYSTEM")
        print("======================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("======================================")

        choice = input("Enter Choice : ").strip()

        # -----------------------------------------------------
        # Register
        # -----------------------------------------------------

        if choice == "1":

            register()

        # -----------------------------------------------------
        # Login
        # -----------------------------------------------------

        elif choice == "2":

            user_email, user_password = login()

            if user_email is not None:

                print("\nLogged in Successfully.")
                print("User :", user_email)

                # =====================================================
                # Import dashboard after successful login
                # Uncomment this when dashboard.py is ready
                # =====================================================

                # from dashboard import dashboard
                # dashboard(user_email, user_password)

        # -----------------------------------------------------
        # Exit
        # -----------------------------------------------------

        elif choice == "3":

            print("\n======================================")
            print("Thank You for using")
            print("EMAIL AUTOMATION SYSTEM")
            print("======================================")

            break

        # -----------------------------------------------------
        # Invalid Choice
        # -----------------------------------------------------

        else:

            print("\nInvalid Choice.")
            print("Please Enter 1, 2 or 3.")