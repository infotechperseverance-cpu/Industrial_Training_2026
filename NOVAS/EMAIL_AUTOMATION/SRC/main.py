from login import login_menu
from reply_ai_voice import  monitor_inbox
import threading
from email_management import email_management_menu
from send_email import process_emails
from email_tracking import tracking_menu
from spam_management import spam_menu
from reports_logs import reports_logs_menu
from template import template_menu
from recipient import recipient_menu
from write_ai_voice import message
from piechart import generate_pie_chart
from voice import speak  

# ---------------- LOGIN ----------------

sender_email, sender_password = login_menu()


if sender_email is None:
    speak("Thank you for using the Email Automation System. Application Closed.")
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

# ---------------- START BACKGROUND EMAIL MONITOR ----------------

voice_thread = threading.Thread(
    target=monitor_inbox,
    args=(sender_email, sender_password),
    daemon=True
 )

voice_thread.start()

# ---------------- MAIN MENU ----------------


while True:

    print("\n========== EMAIL AUTOMATION SYSTEM ==========")
    print("1. Email Management")
    print("2. Send Pending Emails")
    print("3. Email Tracking")
    print("4. Spam Management")
    print("5. Reports & Logs")
    print("6. Templates")
    print("7. recipient management")
    print("8. Voice Message Writing")
    print("9. Pie Chart")
    print("10. Exit")

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
        template_menu()

    elif choice == "7":
        recipient_menu()   

    elif choice == "8":
        message() 

    elif choice == "9":
        generate_pie_chart()


    elif choice == "10":
        speak("\nThank You for using the Email Automation System.")
        break

    else:
        speak("\nInvalid Choice! Please try again.")