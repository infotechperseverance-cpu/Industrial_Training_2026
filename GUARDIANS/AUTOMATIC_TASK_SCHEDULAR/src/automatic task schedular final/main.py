import threading
import runpy
import notification1
import auth
import task_management
import user_settings


def run_autoexecution():
    runpy.run_path("autoexecution.py", run_name="__main__")


def show_main_menu():
    user = auth.get_current_user()
    if user is None:
        return
    while True:
        print("\n=============================")
        print(f"Welcome, {user['name']} ({user['username']})")
        print("=============================")
        print("1. Create Task")
        print("2. View / Edit / Delete Tasks")
        print("3. Search Tasks")
        print("4. View Calendar")
        print("5. Dashboard")
        print("6. Reports & History")
        print("7. Recycle Bin")
        print("8. Backup & Restore")
        print("9. User Settings")
        print("10. Logout")
        print("11. Exit")
        print("=============================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            task_management.create_task()
        elif choice == "2":
            task_management.view_edit_delete_menu()
        elif choice == "3":
            runpy.run_path("search.py", run_name="__main__")
        elif choice == "4":
            runpy.run_path("view_calender.py", run_name="__main__")
        elif choice == "5":
            runpy.run_path("dashboard.py", run_name="__main__")
        elif choice == "6":
            runpy.run_path("report_history.py", run_name="__main__")
        elif choice == "7":
            runpy.run_path("recyclebin.py", run_name="__main__")
        elif choice == "8":
            runpy.run_path("backup_restore.py", run_name="__main__")
        elif choice == "9":
            user_settings.settings_menu_flow()
        elif choice == "10":
            auth.logout_user()
            break
        elif choice == "11":
            print("\nClosing application safely...")
            exit()
        else:
            print("I2"
                  "nvalid choice. Please enter a number between 1 and 11.")


def start_program():
    t1 = threading.Thread(target=run_autoexecution, daemon=True)
    t1.start()

    while True:
        status = auth.login_gate_menu()
        if status is False:
            break
        if auth.is_logged_in():
            show_main_menu()


if __name__ == "__main__":
    start_program()
