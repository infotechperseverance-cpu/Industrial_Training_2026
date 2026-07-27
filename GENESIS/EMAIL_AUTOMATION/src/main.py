# =============================================================================
# FILE NAME   : main.py
# PROJECT     : EMAIL AUTOMATION SYSTEM
# DESCRIPTION : Main menu driven program.
#               Controls all email automation modules.
# =============================================================================
# ========================= IMPORT MODULES =========================
import sys
import login
from ai_email import AIEmailWriter
import Draft_Management
import contactg
import smart_spam
import send_email
import bulk_email
import scheduler
import follow_up
import approval_flow
import emailers
import repoarts
import Dashboard
import retrieved_data

# ========================= GLOBAL VARIABLES =========================
logged_user = None
app_password = None
# =============================================================================
# USER AUTHENTICATION
# =============================================================================
def authentication():
    global logged_user
    global app_password

    while True:
        print("\n==============================")
        print("       AUTHENTICATION")
        print("==============================")
        print("1. Register")
        print("2. Login")
        print("3. Back")

        choice = input("Enter Choice : ")

        if choice == "1":
            login.register()

        elif choice == "2":
            user, password = login.login()

            if user:
                logged_user = user
                app_password = password
                print("\nLogin Successful")
                print("Welcome :", logged_user)
                break

        elif choice == "3":
            break

        else:
            print("Invalid Choice")


# =============================================================================
# AI EMAIL GENERATOR
# =============================================================================
def ai_email_menu():
    writer = AIEmailWriter()

    topic = input("\nEmail Topic : ")
    tone = input("Email Tone : ")
    details = input("Email Details : ")

    subject, body = writer.generate_email(topic, tone, details)

    print("\nGenerated Email")
    print("----------------------------")
    print("Subject :", subject)
    print("\nBody :")
    print(body)


# =============================================================================
# CONTACT MENU
# =============================================================================
def contact_menu():
    contactg.create_tables()

    while True:
        print("\n==============================")
        print(" CONTACT MANAGEMENT")
        print("==============================")
        print("1. Create Group")
        print("2. View Groups")
        print("3. Add Contact")
        print("4. View Contacts")
        print("5. Update Contact")
        print("6. Delete Contact")
        print("7. Delete Group")
        print("8. Back")

        choice = input("Choice : ")

        if choice == "1":
            contactg.create_group()
        elif choice == "2":
            contactg.view_groups()
        elif choice == "3":
            contactg.add_contact()
        elif choice == "4":
            contactg.view_contacts()
        elif choice == "5":
            contactg.update_contact()
        elif choice == "6":
            contactg.delete_contact()
        elif choice == "7":
            contactg.delete_group()
        elif choice == "8":
            break
        else:
            print("Invalid Choice")


# =============================================================================
# MAIN PROGRAM
# =============================================================================
while True:
    print("\n================================================")
    print("      EMAIL AUTOMATION MANAGEMENT SYSTEM")
    print("================================================")
    print("Logged User :", logged_user if logged_user else "Not Logged In")
    print("-----------------------------------------------")

    print("""
1. User Authentication
2. AI Email Generator
3. Draft Management
4. Contact Management
5. Smart Spam Checker
6. Send Single Email
7. Send Bulk Email
8. Schedule Email
9. Follow Up Email
10. Approval Workflow
11. Email Reminder
12. Retrieve Data
13. Reports
14. Dashboard
15. Exit
 """)
    print("---------------------------------------")

    try:
        choice = int(input("Enter Choice : "))
    except:
        print("Invalid Input")
        continue

    # ========================= MENU =========================
    match choice:
        case 1:
            authentication()

        case 2:
            if logged_user:
                ai_email_menu()
            else:
                print("Please Login First")

        case 3:
            Draft_Management.draft_menu()

        case 4:
            contact_menu()

        case 5:
            text = input("\nEnter Email Content : ")
            smart_spam.check_spam_email(text)

        case 6:
            try:
                if logged_user:
                    obj = send_email.SendEmail()
                    obj.send_mail()
                    obj.close_connection()
                else:
                    print("Please Login First")
            except Exception as e:
                print("Send Email Error :", e)

        case 7:
            try:
                obj = bulk_email.BulkEmail()
                obj.run()
                obj.close_connection()
            except Exception as e:
                print("Bulk Email Error :", e)

        case 8:
            if logged_user:
                scheduler.scheduler_menu(logged_user, app_password)
            else:
                print("Please Login First")

        case 9:
            if logged_user:
                follow_up.followup_menu(logged_user, app_password)
            else:
                print("Please Login First")

        case 10:
            approval_flow.create_tables()
            approval_flow.approval_workflow_menu(logged_user, app_password)

        case 11:
            emailers.reminder_menu()

        case 12:
            obj = retrieved_data.RetrieveData()
            obj.retrieve_menu()
            obj.close_connection()

        case 13:
            repoarts.report_menu()

        case 14:
            dashboard = Dashboard.EmailAnalytics()
            dashboard.dashboard()
            dashboard.close_connection()

        case 15:
            print("\nThank You For Using Email Automation System")
            sys.exit()

        case _:
            print("Invalid Choice")
