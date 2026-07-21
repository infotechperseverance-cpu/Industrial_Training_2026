import sys
from datetime import datetime
import login
import send_email
import scheduler
import Follow_up
import BULKEMAILL
import Contactg
import Smart_Spam
import Ai_email
import Draft_Management
import EMAILRS
import REPORTS
import Dashboard
import retrieved_data
import approval_workflow

def authentication_sub_menu():
    """Sub-menu for Authentication (Sign Up / Sign In)"""
    while True:
        print("\n-----------------------------------------")
        print("     1. USER AUTHENTICATION SYSTEM      ")
        print("-----------------------------------------")
        print("1. Sign Up (Register New Account)")
        print("2. Sign In (Login)")
        print("3. Back to Main Menu")
        print("-----------------------------------------")
        
        choice = input("Select Option (1-3): ").strip()
        
        if choice == '1':
            login.register()
        elif choice == '2':
            email, pwd = login.login()
            if email and pwd:
                return email, pwd
            else:
                return None, None
        elif choice == '3':
            return None, None
        else:
            print("\n[Error]: Invalid selection! Choose 1, 2, or 3.")

def contact_sub_menu():
    """Sub-menu for Contact and Group Management"""
    con = Contactg.connect_database()
    if con:
        Contactg.create_tables(con)
        print("\n-----------------------------------------")
        print("    CONTACT & GROUP MANAGEMENT MENU      ")
        print("-----------------------------------------")
        Contactg.menu()
        sub_ch = input("Enter Choice: ").strip()
        
        if sub_ch == "1": Contactg.create_group(con)
        elif sub_ch == "2": Contactg.view_groups(con)
        elif sub_ch == "3": Contactg.add_contact(con)
        elif sub_ch == "4": Contactg.view_contacts(con)
        elif sub_ch == "5": Contactg.update_contact(con)
        elif sub_ch == "6": Contactg.delete_contact(con)
        elif sub_ch == "7": Contactg.delete_group(con)
        con.close()

def main_menu():
    authenticated_user = None
    saved_password = None
    status = "Not Authenticated"
    
    analytics_obj = Dashboard.EmailAnalytics()
    ai_writer = Ai_email.AIEmailWriter()

    while True:
        print("\n==================================================")
        print("        EMAIL AUTOMATION & MANAGEMENT SYSTEM      ")
        print("==================================================")
        print(f"Status: {status}")
        if authenticated_user:
            print(f"Logged In User: {authenticated_user}")
        print("--------------------------------------------------")
        print(" 1. Account Access (Sign Up / Sign In)")
        print(" 2. AI Email Generator (Write Email with AI)")
        print(" 3. Draft Management (Create/Edit Drafts)")
        print(" 4. Contact & Group Management")
        print(" 5. Smart Spam Checker (Quality Score)")
        print(" 6. Send Single Email (with Attachment)")
        print(" 7. Send Bulk Email")
        print(" 8. Schedule Email")
        print(" 9. Send FollowUp Email")
        print("10. Email Approval Workflow (FR-14 - User/Manager)")
        print("11. Email Reminder System")
        print("12. Retrieve Data (Email History, Templates & Drafts)")
        print("13. Analytics Dashboard & Reports")
        print("14. Exit System")
        print("==================================================")
        
        choice = input("Select an Option (1-14): ").strip()
        
        # 1. ACCOUNT ACCESS
        if choice == '1':
            email, pwd = authentication_sub_menu()
            if email and pwd:
                authenticated_user = email
                saved_password = pwd
                status = "Authenticated"
                print(f"\n[Success]: Welcome {authenticated_user}!")

        # ALL OTHER OPTIONS REQUIRE AUTHENTICATION FIRST
        elif choice in [str(i) for i in range(2, 14)] and status != "Authenticated":
            print("\n[Access Denied]: You must Sign In (Option 1) first to perform this action!")

        # 2. AI EMAIL GENERATOR
        elif choice == '2':
            topic = input("Enter Email Topic: ")
            tone = input("Enter Tone (e.g., Formal / Professional / Casual): ")
            details = input("Enter Key Details: ")
            sub, body = ai_writer.generate_email(topic, tone, details)
            print(f"\n--- Generated Subject ---\n{sub}")
            print(f"\n--- Generated Body ---\n{body}")

        # 3. DRAFT MANAGEMENT
        elif choice == '3':
            print("\n--- Draft Management ---")
            Draft_Management.view_drafts()

        # 4. CONTACT & GROUP MANAGEMENT
        elif choice == '4':
            contact_sub_menu()

        # 5. SMART SPAM CHECKER
        elif choice == '5':
            content = input("Enter Email Content to Check Spam Score:\n")
            Smart_Spam.spam_checker(content)

        # 6. SEND SINGLE EMAIL
        elif choice == '6':
            try:
                obj = send_email.SendEmail()
                obj.send_mail()
                obj.close_connection()
            except Exception as e:
                print(f"\n[Error]: {e}")

        # 7. SEND BULK EMAIL
        elif choice == '7':
            BULKEMAILL.send_bulk_email()

        # 8. SCHEDULE EMAIL
        elif choice == '8':
            scheduler.schedule_email(authenticated_user, saved_password)

        # 9. FOLLOW-UP EMAIL
        elif choice == '9':
            try:
                followup = Follow_up.FollowUpEmail()
                followup.display_receivers()
                receiver_id = int(input("Enter Receiver ID : "))
                receiver = followup.get_receiver_email(receiver_id)

                if receiver:
                    subject = input("Enter Subject : ")
                    message = input("Enter Follow-up Message : ")
                    delay = int(input("Enter Delay in Seconds : "))
                    followup.send_followup(receiver, subject, message, delay)
                else:
                    print("[Error]: Invalid Receiver ID")
                followup.close_connection()
            except Exception as e:
                print(f"\n[Error in FollowUp]: {e}")

        # 10. EMAIL APPROVAL WORKFLOW (FR-14)
        elif choice == '10':
            approval_workflow.approval_workflow_menu(authenticated_user, saved_password)

        # 11. EMAIL REMINDER SYSTEM
        elif choice == '11':
            EMAILRS.add_reminder()

        # 12. RETRIEVE DATA & HISTORY
        elif choice == '12':
            obj = retrieved_data.RetrieveData()
            obj.retrieve_menu()

        # 13. ANALYTICS & REPORTS
        elif choice == '13':
            print("\n--- Email Reports & Statistics ---")
            REPORTS.statistics()
            analytics_obj.dashboard()

        # 14. EXIT
        elif choice == '14':
            print("\nExiting Email Automation System. Goodbye!")
            sys.exit()

        else:
            print("\n[Error]: Invalid selection! Please enter a number between 1 and 14.")

if __name__ == "__main__":
    main_menu()
