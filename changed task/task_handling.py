import auth
import task_management
import user_settings

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
        print("3. User Settings & Profile")
        print("4. Logout")
        print("5. Exit")
        print("=============================")        
        choice = input("Enter your choice: ").strip()        
        if choice == "1":
            task_management.create_task()
        elif choice == "2":
            task_management.view_edit_delete_menu()
        elif choice == "3":
            user_settings.settings_menu_flow()
        elif choice == "4":
            auth.logout_user()
            break  
        elif choice == "5":
            print("\nClosing application safely...")
            exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
def start_program():
    while True:
        status = auth.login_gate_menu()
        if status is False:
            break
            
        if auth.is_logged_in():
            show_main_menu()
if __name__ == "__main__":
    start_program()