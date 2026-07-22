import smtplib
import ssl
import time
from datetime import datetime
import threading
from ai_email import AIEmailWriter
import mysql.connector

def db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="system@123",
            database="email_login"
        )
        return connection

    except mysql.connector.Error as err:
        print(f"\nDatabase Error : {err}")
        return None




# FUNCTION NAME: email_checker
# WHAT IT DOES: This function runs in the background. It checks the time 
#               every minute. When time matches, it sends the email.
# INPUTS: sender_email, sender_password, receiver_email, subject, body, user_time
# OUTPUT: None

def email_checker(sender_email, sender_password, receiver_email, subject, body, user_time):
    print(f"\nBackground job started for {receiver_email}. Waiting for time...")
    
    while True:
        my_time = datetime.now()
        
        # changing current time to text format to check easily
        current_time_text = my_time.strftime("%Y-%m-%d %H:%M")
        
        # checking if computer time is same as user time
        if current_time_text == user_time:
            print(f"\nTime reached ({user_time})! Sending email...")
            
            # basic connection variables
            server_name = "smtp.gmail.com"
            server_port = 465
            my_context = ssl.create_default_context()
            msg = f"Subject: {subject}\n\n{body}"
            
            try:
                # connecting to live gmail server
                gmail_server = smtplib.SMTP_SSL(server_name, server_port, context=my_context)
                gmail_server.login(sender_email, sender_password)
                gmail_server.sendmail(sender_email, receiver_email, msg)
                gmail_server.quit()
                
                print(f"\nSuccess: Scheduled email sent to {receiver_email} successfully!")
                break 
                
            except Exception as e:
                print(f"\nFailed to send scheduled email: {e}")
                break 
                
        # waiting for 30 seconds so computer does not get slow or hang
        time.sleep(30)



# FUNCTION NAME: schedule_email
# WHAT IT DOES: Takes inputs from user like email and time. Validates 
#               the time format. Starts a background thread for the email.
# INPUTS: sender_email, sender_password
# OUTPUT: None

def schedule_email(sender_email, sender_password):
    print("\n-----------------------------------------")
    print("         SMART EMAIL SCHEDULER           ")
    print("-----------------------------------------")
    
    if not sender_email or not sender_password:
        print("\nError: Please sign in first to use the Email Scheduler!")
        return

    # taking basic inputs from user
    # taking recipient email
    receiver_email = input("Enter Recipient Email ID: ").strip()

    print("\nEmail Writing Options")
    print("1. Write Email Yourself")
    print("2. Generate Using AI")

    choice = input("Select Option (1-2): ").strip()

    if choice == "1":

        subject = input("Enter Email Subject: ").strip()
        body = input("Enter Email Message Body: ").strip()

    elif choice == "2":

        # Taking email topic and tone from the user
        topic = input("Enter Email Topic: ").strip()
        tone = input("Enter Tone (Professional/Friendly/Formal): ").strip()

        # Variable to store the information required for email generation
        details = ""

        # Asking for required details if the topic is an offer letter
        if topic.lower() == "offer letter":

            candidate_name = input("Enter Candidate Name: ").strip()
            company_name = input("Enter Company Name: ").strip()
            job_title = input("Enter Job Title: ").strip()
            start_date = input("Enter Start Date: ").strip()
            salary = input("Enter Salary: ").strip()
            acceptance_deadline = input("Enter Acceptance Deadline: ").strip()
            sender_name = input("Enter Your Name: ").strip()
            sender_designation = input("Enter Your Designation: ").strip()

            # Combining all user details into a single string
            details = f"""
    Candidate Name: {candidate_name}
    Company Name: {company_name}
    Job Title: {job_title}
    Start Date: {start_date}
    Salary: {salary}
    Acceptance Deadline: {acceptance_deadline}
    Sender Name: {sender_name}
    Sender Designation: {sender_designation}
    """

        else:

            # Taking custom details for other email topics
            details = input("Enter Details: ").strip()

        # Creating an AI email writer object
        writer = AIEmailWriter()

        # Generating the email subject and body using Gemini AI
        subject, body = writer.generate_email(topic, tone, details)

        # Displaying the generated email
        print("\nGenerated Email")
        print("--------------------------------")
        print("Subject:", subject)
        print()
        print("Body:")
        print(body)

    else:
        print("\nInvalid Choice!")
        return

    print("\nEnter Scheduled Date & Time (Format: YYYY-MM-DD HH:MM)")
    user_time = input("Your Target Time: ").strip()

    # checking if any input is empty
    if receiver_email == "" or subject == "" or body == "" or user_time == "":
        print("\nError: All scheduler fields are mandatory!")
        return

    try:
        # checking if date time format is correct or wrong
        datetime.strptime(user_time, "%Y-%m-%d %H:%M")
    except ValueError:
        print("\nError : Invalid Date/Time format! Please use YYYY-MM-DD HH:MM.")
        return



    # -----------------------------
    # Save Scheduled Email
    # -----------------------------

    conn = db_connection()

    if conn:

        cursor = conn.cursor()

        query = """
        INSERT INTO scheduled_emails
        (recipient, subject, body, schedule_time, status)
        VALUES (%s,%s,%s,%s,%s)
        """

        cursor.execute(query, (
            receiver_email,
            subject,
            body,
            user_time,
            "Pending"
        ))

        conn.commit()

        cursor.close()

        conn.close()

    # starting thread so main menu does not freeze or block
    my_thread = threading.Thread(
        target=email_checker,
        args=(sender_email, sender_password, receiver_email, subject, body, user_time)
    )
    
    my_thread.start()
    
    print("\nYour email has been successfully scheduled!")
    print(" You can perform other tasks.")
