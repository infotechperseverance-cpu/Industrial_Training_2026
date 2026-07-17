import login
import sys

# 1. Sub-menu function displayed when the user selects 'User Login'
def login_sub_menu():
    while True:
        print("\n--- LOGIN & REGISTRATION OPTIONS ---")
        print("1. Sign Up (Register New Account)")
        print("2. Sign In (Login to Existing Account)")
        print("3. Back to Main Menu")
        print("------------------------------------")
        
        sub_choice = input("Select an option (1-3): ").strip()
        
        # User wants to create a new account in the database
        if sub_choice == '1':
            login.register()
            
        # User wants to log into the system using existing credentials
        elif sub_choice == '2':
            email, pwd = login.login()
            if email and pwd:
                return email, pwd # Returning successfully authenticated user details
            else:
                return None, None
                
        # User wants to return back to the previous main menu
        elif sub_choice == '3':
            return None, None
            
        else:
            print("\n[Error] Invalid selection! Please enter 1, 2, or 3.")

# 2. Main menu function of entire application flow
def main_menu():
    # Session state variables to keep track of user login status globally
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
        print("1. User Login") 
        print("2. Exit System")
        print("=========================================")
        
        choice = input("Select an option (1-2): ").strip()
        
        # Handling the first menu option to process user authentication
        if choice == '1':
            # Redirecting user into the sub-menu for Sign Up or Sign In choices
            email, pwd = login_sub_menu()
            if email and pwd:
                authenticated_user = email
                status = "Authenticated"
                
        # Handling the second menu option to close the system safely
        elif choice == '2':
            print("\nExiting system safely. Goodbye!")
            sys.exit()
            
        else:
            print("\n[Error] Invalid selection! Please enter 1 or 2.")

if __name__ == "__main__":
    main_menu()
