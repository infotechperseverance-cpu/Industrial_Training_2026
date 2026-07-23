from user_management import login, admin_menu, user_menu
from process import process_menu, user_process_menu
from scheduler import scheduler_menu
from automation import automation_menu
from file_handler import file_handler_menu
from kernel_demo import show_kernel_usage

# ==========================================
# ADMIN DASHBOARD
# ==========================================

def admin_dashboard():

    while True:

        print("\n========== ADMIN DASHBOARD ==========")
        print("1. User Management")
        print("2. Process Management")
        print("3. Scheduler")
        print("4. Automation")
        print("5. File Handler")
        print("6.Show kernel space")
        print("7.Logout")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            admin_menu()

        elif choice == "2":

            process_menu()

        elif choice == "3":

            scheduler_menu()

        elif choice == "4":

            automation_menu()

        elif choice == "5":

            file_handler_menu()
        elif choice == "6":

    show_kernel_usage()

        elif choice == "7":

            print("\nLogged Out Successfully.")
            break

        else:

            print("Invalid Choice.")


# ==========================================
# USER DASHBOARD
# ==========================================

def user_dashboard(user_id):

    while True:

        print("\n========== USER DASHBOARD ==========")
        print("1. My Tasks")
        print("2. Process")
        print("3. File Handler")
        print("4. Logout")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            user_menu(user_id)

        elif choice == "2":

            user_process_menu()

        elif choice == "3":

            file_handler_menu()

        elif choice == "4":

            print("\nLogged Out Successfully.")
            break

        else:

            print("Invalid Choice.")


# ==========================================
# LOGIN
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

        admin_dashboard()

    else:

        user_dashboard(user_id)


# ==========================================
# MAIN
# ==========================================

def main():

    while True:

        print("\n========== PROCESS AUTOMATION SYSTEM ==========")
        print("1. Login")
        print("2. Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            start()

        elif choice == "2":

            print("\nThank You for Using Process Automation System.")
            break

        else:

            print("Invalid Choice.")


if __name__ == "__main__":

    main()