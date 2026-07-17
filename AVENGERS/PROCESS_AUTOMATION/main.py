import csv
import datetime

# Desktop Notification (Optional)
try:
    from plyer import notification
    desktop = True
except:
    desktop = False


# -------------------------------
# Notification Function
# -------------------------------
def send_notification(title, message):
    print(f"\n{title}")
    print(message)

    if desktop:
        notification.notify(
            title=title,
            message=message,
            timeout=5
        )


# -------------------------------
# Log Function
# -------------------------------
def save_log(username, action):
    with open("logs.txt", "a") as file:
        file.write(f"{datetime.datetime.now()} - {username} - {action}\n")


# -------------------------------
# Login Function
# -------------------------------
def login():

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    with open("users.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if row["username"] == username and row["password"] == password:

                print("\nLogin Successful")
                print("Role :", row["role"])

                save_log(username, "Login")

                send_notification(
                    "Login",
                    "Login Successful"
                )

                return username

    print("\nInvalid Username or Password")
    return None


# -------------------------------
# Logout Function
# -------------------------------
def logout(username):

    if username:

        save_log(username, "Logout")

        send_notification(
            "Logout",
            "Logout Successful"
        )

        print("Logged Out Successfully")

    else:
        print("No user logged in.")


# -------------------------------
# Main Menu
# -------------------------------
current_user = None

while True:

    print("\n===== PROCESS AUTOMATION =====")
    print("1. Login")
    print("2. Logout")
    print("3. Exit")

    choice = input("Enter Choice : ")

    if choice == "1":
        current_user = login()

    elif choice == "2":
        logout(current_user)
        current_user = None

    elif choice == "3":
        print("Thank You")
        break

    else:
        print("Invalid Choice")