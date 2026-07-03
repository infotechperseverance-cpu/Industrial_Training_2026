import json
import os
from datetime import datetime
import hashlib

FILE_NAME = "users.json"


def load_json():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

    return []


def save_json(users):
    with open(FILE_NAME, "w") as f:
        json.dump(users, f, indent=4)


def check_email(email):
    return "@" in email and email.endswith(".com")


def hashing(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    users = load_json()

    full_name = input("Enter Full Name: ")
    username = input("Enter Username: ")

    email = input("Enter Email: ")
    while not check_email(email):
        print("Invalid Email Format!")
        email = input("Enter Email: ")

    password = input("Enter Password: ")
    hashed_password = hashing(password)

    
    for user in users:
        if user["username"] == username:
            print("Username already exists!")
            return

        if user["email"] == email:
            print("Email already registered!")
            return

    user = {
        "user_id": len(users) + 1,
        "full_name": full_name,
        "username": username,
        "email": email,
        "password": hashed_password,
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "last_login": ""
    }

    users.append(user)
    save_json(users)

    print("Registration Successful!")


def login():
    users = load_json()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    hashed_password = hashing(password)

    for user in users:
        if user["username"] == username and user["password"] == hashed_password:
            print("\nLogin Successful!")
            print("Welcome,", user["full_name"])

            user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_json(users)
            return

    print("Invalid Username or Password")


def main():
    while True:
        print("\n===== USER MANAGEMENT SYSTEM =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            register()

        elif choice == "2":
            login()

        elif choice == "3":
            print("Thank You!")
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()
