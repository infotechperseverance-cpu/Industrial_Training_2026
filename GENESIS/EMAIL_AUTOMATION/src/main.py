import login
import scheduler
import send_email
import follow_up
import attachment
import sys
import retrieved_data

# 1. Sub-menu function displayed when the user selects 'User Login'
def login_sub_menu():
    while True:
        print("\n--- LOGIN & REGISTRATION OPTIONS ---")
        print("1. Sign Up ")
        print("2. Sign In ")
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
            print("\nError: Invalid selection! Please enter 1, 2, or 3.")

# 2. Main menu function of entire application flow
def main_menu():
    # Session state variables to keep track of user login status globally
    authenticated_user = None
    saved_password = None # Storing password for scheduler use
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
        print("2.Send Email ")
        print("3. Schedule an Email")
        print("4. Retrieve data")
        print("5. FollowUp Email")
        print("6. Exit ") 
        print("=========================================")
        
        choice = input("Select an option : ").strip()
        
        # Handling the first menu option to process user authentication
        if choice == '1':
            # Redirecting user into the sub-menu for Sign Up or Sign In choices
            email, pwd = login_sub_menu()
            if email and pwd:
                authenticated_user = email
                saved_password = pwd # Saving password safely
                status = "Authenticated"
        elif choice == "2":
           if status == "Authenticated":
            obj = send_email.SendEmail()
            obj.send_mail()
           else:
            print("\nPlease login first.")       
        # Handling the second menu option to run the email scheduler
        elif choice == '3':
            if status == "Authenticated":
                scheduler.schedule_email(authenticated_user, saved_password)
            else:
                print("\nError: You must log in first before scheduling emails!")
                
        elif choice == "4":
            if status == "Authenticated":
                obj = retrieved_data.RetrieveData()
                obj.retrieve_menu()
            else:
                print("\nPlease login first.")
        elif choice == "5":
            if status == "Authenticated":
              follow_up.send_followup()
            else:
              print("\nPlease login first.")
        elif choice == "6":
            print("\nExiting System...")
            sys.exit()
            
        else:
            print("\nError: Invalid selection! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
