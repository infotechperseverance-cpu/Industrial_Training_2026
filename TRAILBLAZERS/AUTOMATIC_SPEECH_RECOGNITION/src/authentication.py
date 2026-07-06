import json
import os
import re
from config import USERS_FILE
from voice_engine import speak



# Create users.json if it does not exist
def initialize_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as file:
            json.dump([], file, indent=4)

# Load users from JSON
def load_users():
    initialize_users_file()
    try:
        with open(USERS_FILE, "r") as file:
            users = json.load(file)
            if isinstance(users, list):
                return users

            return []

    except json.JSONDecodeError:
        with open(USERS_FILE, "w") as file:
            json.dump([], file, indent=4)

        return []

    except Exception:

        return []


# Save users
def save_users(users):

    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


# Username Validation
def validate_username(username):

    username = username.strip()

    if username == "":
        return False, "Username cannot be empty."

    if len(username) < 4:
        return False, "Username must be at least 4 characters."

    if len(username) > 20:
        return False, "Username cannot exceed 20 characters."

    pattern = r"^[A-Za-z][A-Za-z0-9_]*$"

    if not re.match(pattern, username):
        return False, "Username should start with a letter and contain only letters, numbers and underscore."

    return True, "Valid"


# Password Validation
def validate_password(password):

    if password == "":
        return False, "Password cannot be empty."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if len(password) > 20:
        return False, "Password cannot exceed 20 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain one lowercase letter."

    if not re.search(r"[0-9]", password):
        return False, "Password must contain one digit."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain one special character."

    if " " in password:
        return False, "Password cannot contain spaces."

    return True, "Valid"

# Check whether username already exists
def username_exists(username):
    users = load_users()
    for user in users:
        if user["username"].lower() == username.lower():
            return True

    return False

    # Verify login credentials
def verify_credentials(username, password):
    users = load_users()

    for user in users:
        if user["username"] == username and user["password"] == password:
            return True

    return False

    # Create User
def create_user():

    print("\n========== CREATE USER ==========")
    username = input("Enter Username: ").strip()
    valid, message = validate_username(username)
    if not valid:
        print(message)
        return

    if username_exists(username):
        print("Username already exists.")
        return

    password = input("Enter Password: ").strip()

    valid, message = validate_password(password)

    if not valid:
        print(message)
        return

    confirm_password = input("Confirm Password: ").strip()

    if password != confirm_password:
        print("Passwords do not match.")
        return

    users = load_users()

    users.append({ "username": username, "password": password  })

    save_users(users)

    print("User created successfully.")

# Login User
# Login User
def login_user():

    print("\n========== LOGIN ==========")

    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:

        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        if username == "" or password == "":
            print("Username and Password cannot be empty.")
            attempts += 1
            print(f"Attempts Remaining: {max_attempts - attempts}")
            continue

        if verify_credentials(username, password):

            global current_user
            current_user = username

            print("Login Successful.")
            speak(f"Welcome {username}")

            return username

        else:

            attempts += 1

            print("Invalid Username or Password.")

            if attempts < max_attempts:
                print(f"Attempts Remaining: {max_attempts - attempts}")
                speak("Invalid username or password. Please try again.")

    print("\nMaximum login attempts exceeded.")
    speak("Maximum login attempts exceeded.")
    return None


# Logout User


current_user = None

def logout_user():

    global current_user

    if current_user:
        print(f"{current_user} logged out successfully.")
        speak("You have been logged out successfully.")
        current_user = None
        return True

    print("No user is currently logged in.")
    speak("No user is currently logged in.")
    return False


# Authentication Menu
def authentication_menu():

    while True:

        print("\n===================================")
        print("      USER AUTHENTICATION")
        print("===================================")
        print("1. Create User")
        print("2. Login")
        print("3. Exit")
        print("===================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            create_user()

        elif choice == "2":

            current_user = login_user()

            if current_user is not None:
                return current_user

        elif choice == "3":

            print("Exiting Authentication Module.")
            return None

        else:

            print("Invalid choice. Please enter 1, 2 or 3.")


# Main Function (Testing Only)
if __name__ == "__main__":

    current_user = authentication_menu()

    if current_user is not None:

        print(f"\nWelcome, {current_user}!")

        # Your voice assistant will start here later.
        # Example:
        # voice_assistant()

        # Logout after assistant exits
        logout_user(current_user)