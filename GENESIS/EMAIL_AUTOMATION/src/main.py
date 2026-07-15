import login
import sys

def main_menu():
    # Session states to track login status
    authenticated_user = None
    status = "Not Authenticated"
    
    while True:
        print("\n=========================================")
        print("         EMAIL AUTOMATION SYSTEM         ")
        print("=========================================")
        print(f"Status: {status}")
        if authenticated_user:
            print(f"Logged in as: {authenticated_user}")
        print("-----------------------------------------")
        print("1. User Login (FR-01)")
        print("2. Exit System")
        print("=========================================")
        
        choice = input("Select an option (1-2): ").strip()
        
        if choice == '1':
            # Calls the login() function from login.py module
            email, pwd = login.login()
            if email and pwd:
                authenticated_user = email
                status = "Authenticated"
                
        elif choice == '2':
            print("\nExiting system safely. Goodbye!")
            sys.exit()
            
        else:
            print("\n[Error] Invalid selection! Please enter 1 or 2.")

if __name__ == "__main__":
    main_menu()