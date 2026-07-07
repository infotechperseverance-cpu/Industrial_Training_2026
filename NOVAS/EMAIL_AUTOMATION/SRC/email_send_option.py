
import json
import smtplib
from email.message import EmailMessage
from email_utils import load_email_records, save_email_records,validate_email
from send_email import process_single_email,process_emails
from voice import speak
from attachment_utils import add_attachments_to_email
from reports_logs import save_log
from email_tracking import load_email_history, save_email_history
from datetime import datetime
import csv
import os

FILE_NAME = "email_records.json"
BULK_FILE = "bulk_email.csv"

def single_email_send(sender_email, sender_password):
    while True:
      
      if sender_email is None:
          print("Login required.")
          return
      
      memail = input("Enter Email : ").strip()

      if not validate_email(memail):
        speak("Please enter a valid email address.")
        continue
      
      with open(FILE_NAME, "r", encoding="utf-8") as file:
        file_contents = json.load(file)
       
      if isinstance(file_contents, dict):
        file_contents = [file_contents]

      email_found = False

      for record in file_contents:
        
        if record["recipient_email"].lower() == memail.lower():
            email_found = True

            if record.get("status", "").lower() == "pending":
               process_single_email(
                            record,
                            sender_email,
                            sender_password,
                            file_contents
                        )
               return

                

            speak("This email is not in pending status.")
            break

      if not email_found:
        speak("Email not found. Please try again.")

      if sender_email is None:
        print("Login required.")
        return 
      
def multiple_email_send(sender_email, sender_password):
   if sender_email is None:
        print("Login required.")
        return
   speak("Send All Email Its pending")
   process_emails(sender_email, sender_password)


def Bulk_email_send(sender_email, sender_password):

  if sender_email is None:
        print("Login required.")
        return
   
  if not os.path.exists(BULK_FILE):
      speak("File Does Not Exist")
      return
  if os.path.getsize(BULK_FILE) == 0:
        speak("File is empty")
        return
   
  
  with open(BULK_FILE, "r", newline="") as file:
      reader = csv.DictReader(file)
   
      for row in reader:
        if not row:
           continue

        email = row["Email"].strip()
        if not validate_email(email):
            print(f"Invalid email: {email}")
            continue

        print(f"\nEmail: {email}")
        subject = input("Enter Subject: ")
        message = input("Enter message for this email: ")
        attachments = input("Enter attachment paths (comma separated, leave blank if none): ").strip()
        
        
        print("\n----------- Email Preview -----------")
        print(f"Recipient   : {email}")
        print(f"Subject     : {subject}")
        print(f"Message     : {message}")

        if attachments:
            print(f"Attachments : {attachments}")
        else:
            print("Attachments : None")

        confirm = input("\nSend this email? (Y/N): ").strip().lower()

        if confirm != "y":
            print("Email skipped.")
            continue
            
        success = send_email(
          sender_email,
          sender_password,
          email,
          subject,
          message,
          attachments
        )
        if success:
            save_bulk_email(email, subject, message, attachments)
  speak("All emails sent successfully.")


def cbulk_email_send(sender_email, sender_password):
    if sender_email is None:
        print("Login required.")
        return

    if not os.path.exists(BULK_FILE):
        speak("File Does Not Exist")
        return
    if os.path.getsize(BULK_FILE) == 0:
        speak("File is empty")
        return

    subject = input("Enter Subject: ")
    message = input("Enter Message:")
    attachments = input("Enter attachment paths (comma separated, leave blank if none): ").strip()

    print("\n----------- Email Preview -----------")
    print("Recipient   : All recipients in bulk file")
    print(f"Subject     : {subject}")
    print(f"Message     : {message}")

    if attachments:
        print(f"Attachments : {attachments}")
    else:
        print("Attachments : None")

    confirm = input("\nSend this email? (Y/N): ").strip().lower()

    if confirm != "y":
        print("Email skipped.")
        return
    
    with open(BULK_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row:
                continue

            email = row["Email"].strip()
            if not validate_email(email):
                print(f"Invalid email: {email}")
                continue

            success = send_email(
              sender_email,
              sender_password,
              email,
              subject,
              message,
              attachments
            )
            if success:
                save_bulk_email(email, subject, message, attachments)
    speak("All emails sent successfully.")

def save_bulk_email(email, subject, message, attachments):

    save_log(email, "Bulk Email Sent")

    history = load_email_history()

    history.append({
        "email_id": f"Bulk-{email}",
        "recipient_email": email,
        "subject": subject,
        "template_name": "",
        "message": message,
        "attachments": attachments,
        "status": "Completed",
        "sent_date": datetime.now().strftime("%Y-%m-%d"),
        "sent_time": datetime.now().strftime("%H:%M:%S")
    })

    save_email_history(history)


def send_email(sender_email, sender_password, receiver_email, subject, message, attachments):
    try:
        email = EmailMessage()
        email["From"] = sender_email
        email["To"] = receiver_email
        email["Subject"] = subject
        email.set_content(message)

        add_attachments_to_email(email, attachments)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email)

        return True

    except Exception as e:
        print("Error:", e)
        return False

def sending_menu(sender_email, sender_password):

    while True:

        speak("\n---------- Sending Option -----------")
        print("1. Send Single Email")
        print("2. Send Multiple Email")
        print("3. Send Personalized Bulk Email")
        print("4. Send Common Bulk Email")
        print("5. Back")

        choice = input("\nEnter Choice: ")

        if choice == "1":
            try:
                single_email_send(sender_email, sender_password)
            except Exception as e:
                print(f"Error occurred while sending emails: {e}")

        elif choice == "2":
            try:
                multiple_email_send(sender_email, sender_password)
            except Exception as e:
                print(f"Error occurred while sending emails: {e}")

        elif choice == "3":
            try:
                Bulk_email_send(sender_email, sender_password)
            except Exception as e:
                print(f"Error occurred while sending emails: {e}")

        elif choice == "4":
            try:
                cbulk_email_send(sender_email, sender_password)
            except Exception as e:
                print(f"Error occurred while sending emails: {e}")

        elif choice == "5":
            break

        else:
            print("Invalid Choice! Please try again.")
