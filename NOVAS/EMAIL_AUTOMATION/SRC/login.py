import csv
import os
from voice import speak

USER_FILE = "user_data.csv"


# ---------------- CREATE USER FILE ----------------

def create_user_file():

    if not os.path.exists(USER_FILE):

        with open(USER_FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow(
                ["email", "login_password", "smtp_password"]
            )


# ---------------- SIGN UP ----------------

def signup():

    create_user_file()

    print("\n========== SIGN UP ==========")

    email = input("Enter Gmail Address : ")

    login_password = input("Create Login Password : ")

    smtp_password = input("Enter Gmail App Password : ")

    with open(USER_FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["email"] == email:

                print("Account already exists.")
                speak("Account already exists.")


                return

    with open(USER_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(
            [email, login_password, smtp_password]
        )

    print("Account created successfully.")
    speak("Account created successfully.")


# ---------------- LOGIN ----------------

def login():

    create_user_file()

    attempts = 3

    while attempts > 0:

        
        print("\n========== LOGIN ==========")

        email = input("Email : ")

        login_password = input("Password : ")

        stop = input("Do You Want To Stop(stop):").lower()

        if stop == "stop":
            return

        with open(USER_FILE, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if (row["email"] == email and
                        row["login_password"] == login_password):

                    print("\nLogin Successful." \
                    " WELCOME To Email Automation system")
                    speak("\nLogin Successful." \
                    " WELCOME To Email Automation system")

                    return row["email"], row["smtp_password"]

        attempts -= 1

        print("Invalid Email or Password.")

        if attempts > 0:

            print("Attempts Left :", attempts)

    print("\nToo many failed attempts.")

    return None, None


# ---------------- LOGIN MENU ----------------

def login_menu():

    create_user_file()

    while True:

        speak(" EMAIL AUTOMATION LOGIN ")
        print("\n===================================")
        print(" EMAIL AUTOMATION LOGIN ")
        print("===================================")
        print("1. Login")
        print("2. Sign Up / Register")
        print("3. Exit")

        choice = input("Enter Choice : ")

        if choice == "1":

            email, smtp_password = login()
        
            if email is not None:

                return email, smtp_password

        elif choice == "2":

            signup()

        elif choice == "3":

            return None, None

        else:

            speak("Invalid Choice.")
            print("Invalid Choice.")