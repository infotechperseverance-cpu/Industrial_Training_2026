from login import login_menu
from email_management import email_management_menu
from send_email import process_emails
from email_tracking import tracking_menu
from spam_management import spam_menu
from reports_logs import reports_logs_menu


# ---------------- LOGIN ----------------

sender_email, sender_password = login_menu()

if sender_email is None:
    print("\nApplication Closed.")
    exit()


# ---------------- WELCOME MESSAGE ----------------

print("\n==============================================")
print("      EMAIL AUTOMATION SYSTEM")
print("==============================================")
print("\nInstructions:")
print("• Before sending emails, compose your email details in 'email_records.json'.")
print("• Only emails with status 'pending' will be sent.")
print("==============================================")


# ---------------- MAIN MENU ----------------

while True:

    print("\n========== EMAIL AUTOMATION SYSTEM ==========")
    print("1. Email Management")
    print("2. Send Pending Emails")
    print("3. Email Tracking")
    print("4. Spam Management")
    print("5. Reports & Logs")
    print("6. Exit")

    choice = input("\nEnter Choice: ")

    if choice == "1":
        email_management_menu()

    elif choice == "2":
        try:
            process_emails(sender_email, sender_password)
        except Exception as e:
            print(f"Error occurred while sending emails: {e}")

    elif choice == "3":
        tracking_menu()

    elif choice == "4":
        spam_menu()

    elif choice == "5":
        reports_logs_menu()

    elif choice == "6":
        print("\nThank You for using the Email Automation System.")
        break

    else:
        print("\nInvalid Choice! Please try again.")