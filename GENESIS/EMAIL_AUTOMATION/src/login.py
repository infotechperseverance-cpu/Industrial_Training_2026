"""
==============================================================================
                            LOGIN MODULE
==============================================================================
Project Name : Email Automation System
Module Name  : login.py
Description  : User Registration, Login, MySQL Connection, Gmail Validation,
               and Password Masking.
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
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        connection.commit()
    except Error as e:
        print("\nDatabase Creation Error")
        print(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


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
            user_id VARCHAR(150) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
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


def check_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'
    return bool(re.fullmatch(pattern, email))


def get_password(prompt="Enter Password : "):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        ch = msvcrt.getch()
        if ch in (b'\r', b'\n'):
            print()
            break
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


def register():
    create_table()
    print("\n======================================")
    print("         USER REGISTRATION")
    print("======================================")

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

    while True:
        password = get_password("Enter Gmail App Password : ")
        password = password.replace(" ", "")
        if password == "":
            print("\nPassword cannot be empty.")
            continue
        if len(password) != 16:
            print("\nInvalid Gmail App Password.")
            print("App Password must contain exactly 16 characters.")
            continue
        break

    conn = db_connection()
    if conn is None:
        return False
    cursor = None

    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT id FROM users WHERE user_id=%s", (email,))
        record = cursor.fetchone()

        if record:
            print("\n======================================")
            print("ACCOUNT ALREADY EXISTS")
            print("======================================")
            print("This Gmail ID is already registered.")
            return False

        cursor.execute(
            "INSERT INTO users(user_id, password) VALUES(%s, %s)",
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


def login():
    create_table()
    print("\n======================================")
    print("            USER LOGIN")
    print("======================================")

    email = input("Enter Gmail ID : ").strip()
    if email == "":
        print("\nEmail cannot be empty.")
        return None, None

    if not check_email(email):
        print("\nInvalid Gmail ID.")
        print("Please enter a valid Gmail address.")
        return None, None

    conn = db_connection()
    if conn is None:
        return None, None
    cursor = None

    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT password FROM users WHERE user_id=%s", (email,))
        record = cursor.fetchone()

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

        password = get_password("Enter Gmail App Password : ")
        password = password.replace(" ", "")

        if password == "":
            print("\nPassword cannot be empty.")
            return None, None

        stored_password = record[0]
        if password != stored_password:
            print("\n======================================")
            print("LOGIN FAILED")
            print("======================================")
            print("Incorrect App Password.")
            return None, None

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

        if choice == "1":
            register()
        elif choice == "2":
            user_email, user_password = login()
            if user_email is not None:
                print("\nLogged in Successfully.")
                print("User :", user_email)
        elif choice == "3":
            print("\n======================================")
            print("Thank You for using")
            print("EMAIL AUTOMATION SYSTEM")
            print("======================================")
            break
        else:
            print("\nInvalid Choice.")
            print("Please Enter 1, 2 or 3.")
