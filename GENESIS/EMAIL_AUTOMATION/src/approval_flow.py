# =============================================================================
# FILE NAME : approval.py
#
# PROJECT : Email Automation System
#
# MODULE :
# Email Approval Workflow System
#
# DESCRIPTION :
# This module allows users to submit emails for approval.
# Manager can approve/reject emails.
# Approved emails are sent through Gmail SMTP.
#
# DATABASE :
# email_automation
#
# TABLES :
# email_approvals
# email_reports
#
# =============================================================================


import re
import smtplib

import mysql.connector


from mysql.connector import Error

from email.message import EmailMessage

from datetime import datetime



# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================


HOST = "localhost"

USER = "root"

PASSWORD = "root123"      # Change according to MySQL password

DATABASE = "email_automation"




# =============================================================================
# FUNCTION NAME : db_connection
#
# PURPOSE :
# Creates MySQL database connection.
#
# RETURNS :
# Connection Object
#
# =============================================================================


def db_connection():


    try:


        connection = mysql.connector.connect(


            host=HOST,

            user=USER,

            password=PASSWORD,

            database=DATABASE


        )


        return connection



    except Error as err:


        print("\n================================")

        print("DATABASE CONNECTION ERROR")

        print("================================")

        print(err)


        return None





# =============================================================================
# FUNCTION NAME : check_email
#
# PURPOSE :
# Validates Gmail ID.
#
# RETURNS :
# True / False
#
# =============================================================================


def check_email(email):


    pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'


    return bool(re.fullmatch(pattern, email))





# =============================================================================
# FUNCTION NAME : create_tables
#
# PURPOSE :
# Creates required tables.
#
# TABLES:
# 1. email_approvals
# 2. email_reports
#
# =============================================================================


def create_tables():


    conn = db_connection()


    if conn is None:


        return



    cursor = None



    try:



        cursor = conn.cursor(buffered=True)



        # -------------------------------------------------------------
        # EMAIL APPROVAL TABLE
        # -------------------------------------------------------------


        cursor.execute("""


        CREATE TABLE IF NOT EXISTS email_approvals

        (

            id INT AUTO_INCREMENT PRIMARY KEY,


            sender_email VARCHAR(255),


            receiver_email VARCHAR(255),


            subject VARCHAR(255),


            body TEXT,


            status VARCHAR(50)

            DEFAULT 'Pending',


            created_at DATETIME

            DEFAULT CURRENT_TIMESTAMP


        )


        """)



        # -------------------------------------------------------------
        # EMAIL REPORT TABLE
        # Dashboard Integration
        # -------------------------------------------------------------


        cursor.execute("""


        CREATE TABLE IF NOT EXISTS email_reports

        (

            id INT AUTO_INCREMENT PRIMARY KEY,


            recipient_email VARCHAR(255),


            subject VARCHAR(255),


            status VARCHAR(50),


            sent_date DATETIME

            DEFAULT CURRENT_TIMESTAMP


        )


        """)



        conn.commit()



    except Error as err:


        print("\nTable Creation Error")

        print(err)



    finally:



        if cursor:


            cursor.close()



        conn.close()

# =============================================================================
# FUNCTION NAME : request_email_approval
#
# PURPOSE :
# Allows user to submit an email request for manager approval.
#
# INPUT :
# sender_email
#
# =============================================================================


def request_email_approval(sender_email):


    print("\n===================================")

    print("      SUBMIT EMAIL FOR APPROVAL")

    print("===================================")



    receiver_email = input(

        "Receiver Email : "

    ).strip()



    if not check_email(receiver_email):


        print("\nInvalid Receiver Gmail ID.")

        return




    subject = input(

        "Subject : "

    ).strip()



    body = input(

        "Message Body : "

    ).strip()




    if subject == "" or body == "":


        print("\nSubject and Message cannot be empty.")

        return





    conn = db_connection()



    if conn is None:


        return




    cursor = None



    try:



        cursor = conn.cursor(buffered=True)



        query = """


        INSERT INTO email_approvals


        (

            sender_email,

            receiver_email,

            subject,

            body,

            status


        )


        VALUES


        (

            %s,

            %s,

            %s,

            %s,

            'Pending'


        )


        """




        cursor.execute(

            query,

            (

                sender_email,

                receiver_email,

                subject,

                body

            )

        )




        conn.commit()



        print("\nEmail submitted successfully.")

        print("Status : Pending")



    except Error as err:



        print("\nSubmission Error")

        print(err)



    finally:



        if cursor:


            cursor.close()



        conn.close()






# =============================================================================
# FUNCTION NAME : view_pending_emails
#
# PURPOSE :
# Displays all pending email requests.
#
# RETURNS :
# Selected email details
#
# =============================================================================


def view_pending_emails():


    conn = db_connection()



    if conn is None:


        return []



    cursor = None



    try:



        cursor = conn.cursor(buffered=True)



        cursor.execute("""


        SELECT


            id,


            sender_email,


            receiver_email,


            subject,


            body


        FROM email_approvals


        WHERE status='Pending'


        ORDER BY created_at



        """)



        records = cursor.fetchall()




        print("\n===================================")

        print("       PENDING EMAIL REQUESTS")

        print("===================================")



        if len(records) == 0:


            print("No Pending Requests Found.")



        else:



            for row in records:



                print("-----------------------------------")

                print("ID       :", row[0])

                print("From     :", row[1])

                print("To       :", row[2])

                print("Subject  :", row[3])




        return records




    except Error as err:



        print("\nFetch Error")

        print(err)



        return []



    finally:



        if cursor:


            cursor.close()



        conn.close()






# =============================================================================
# FUNCTION NAME : get_email_request
#
# PURPOSE :
# Gets selected pending email details.
#
# INPUT :
# request_id
#
# RETURNS :
# Email Details
#
# =============================================================================


def get_email_request(request_id):


    conn = db_connection()



    if conn is None:


        return None




    cursor = None



    try:



        cursor = conn.cursor(buffered=True)



        cursor.execute("""


        SELECT


            sender_email,


            receiver_email,


            subject,


            body



        FROM email_approvals



        WHERE id=%s


        AND status='Pending'



        """,

        (request_id,)



        )



        result = cursor.fetchone()



        return result




    except Error as err:



        print("\nRequest Fetch Error")

        print(err)



        return None




    finally:



        if cursor:


            cursor.close()



        conn.close()

# =============================================================================
# FUNCTION NAME : save_email_report
#
# PURPOSE :
# Saves approved email details into email_reports table.
#
# =============================================================================


def save_email_report(receiver_email, subject, status):


    conn = db_connection()


    if conn is None:


        return



    cursor = None



    try:


        cursor = conn.cursor(buffered=True)



        cursor.execute("""


        INSERT INTO email_reports


        (

            recipient_email,

            subject,

            status


        )


        VALUES


        (

            %s,

            %s,

            %s


        )


        """,

        (

            receiver_email,

            subject,

            status

        )

        )



        conn.commit()



    except Error as err:


        print("\nReport Saving Error")

        print(err)



    finally:


        if cursor:


            cursor.close()



        conn.close()





# =============================================================================
# FUNCTION NAME : update_status
#
# PURPOSE :
# Updates approval request status.
#
# =============================================================================


def update_status(request_id, status):


    conn = db_connection()



    if conn is None:


        return




    cursor = None



    try:



        cursor = conn.cursor(buffered=True)



        cursor.execute("""


        UPDATE email_approvals


        SET status=%s


        WHERE id=%s



        """,

        (

            status,

            request_id

        )

        )



        conn.commit()



    except Error as err:



        print("\nStatus Update Error")

        print(err)



    finally:



        if cursor:


            cursor.close()



        conn.close()





# =============================================================================
# FUNCTION NAME : send_approved_email
#
# PURPOSE :
# Sends approved email through Gmail SMTP.
#
# =============================================================================


def send_approved_email(

        sender_email,

        app_password,

        receiver_email,

        subject,

        body

):


    try:



        email = EmailMessage()



        email["From"] = sender_email


        email["To"] = receiver_email


        email["Subject"] = subject



        email.set_content(body)



        server = smtplib.SMTP(

            "smtp.gmail.com",

            587

        )



        server.starttls()



        server.login(

            sender_email,

            app_password

        )



        server.send_message(email)



        server.quit()



        return True



    except Exception as err:



        print("\nEmail Sending Error")

        print(err)



        return False






# =============================================================================
# FUNCTION NAME : manager_panel
#
# PURPOSE :
# Manager approves or rejects email requests.
#
# =============================================================================


def manager_panel(manager_email, manager_password):


    print("\n===================================")

    print("        MANAGER APPROVAL PANEL")

    print("===================================")



    requests = view_pending_emails()



    if len(requests) == 0:


        return




    request_id = input(

        "\nEnter Email Request ID : "

    ).strip()



    if not request_id.isdigit():


        print("Invalid ID.")

        return




    email_data = get_email_request(request_id)



    if email_data is None:


        print("\nEmail Request Not Found.")

        return




    sender = email_data[0]

    receiver = email_data[1]

    subject = email_data[2]

    body = email_data[3]




    action = input(

        "\nApprove or Reject (A/R): "

    ).upper()




    if action == "A":



        result = send_approved_email(

            manager_email,

            manager_password,

            receiver,

            subject,

            body

        )



        if result:



            update_status(

                request_id,

                "Approved"

            )



            save_email_report(

                receiver,

                subject,

                "Success"

            )



            print("\nEmail Approved and Sent Successfully.")



        else:



            update_status(

                request_id,

                "Failed"

            )



            save_email_report(

                receiver,

                subject,

                "Failed"

            )





    elif action == "R":



        update_status(

            request_id,

            "Rejected"

        )



        print("\nEmail Request Rejected.")



    else:


        print("\nInvalid Option.")





# =============================================================================
# FUNCTION NAME : approval_workflow_menu
#
# PURPOSE :
# Main approval module menu.
#
# =============================================================================


def approval_workflow_menu(user_email=None, password=None):


    if user_email is None:


        user_email = input(

            "Enter Gmail ID : "

        )



        password = input(

            "Enter App Password : "

        )




    while True:



        print("\n===================================")

        print("      EMAIL APPROVAL WORKFLOW")

        print("===================================")

        print("1. Submit Email For Approval")

        print("2. Manager Approval Panel")

        print("3. Exit")

        print("===================================")



        choice = input(

            "Enter Choice : "

        )




        if choice == "1":


            request_email_approval(

                user_email

            )



        elif choice == "2":


            manager_panel(

                user_email,

                password

            )



        elif choice == "3":


            break



        else:


            print("Invalid Choice.")





# =============================================================================
# MAIN PROGRAM
# =============================================================================


if __name__ == "__main__":


    create_tables()



    approval_workflow_menu()# =============================================================================
# FUNCTION NAME : save_email_report
#
# PURPOSE :
# Saves approved email details into email_reports table.
#
# =============================================================================


def save_email_report(receiver_email, subject, status):


    conn = db_connection()


    if conn is None:


        return



    cursor = None



    try:


        cursor = conn.cursor(buffered=True)



        cursor.execute("""


        INSERT INTO email_reports


        (

            recipient_email,

            subject,

            status


        )


        VALUES


        (

            %s,

            %s,

            %s


        )


        """,

        (

            receiver_email,

            subject,

            status

        )

        )



        conn.commit()



    except Error as err:


        print("\nReport Saving Error")

        print(err)



    finally:


        if cursor:


            cursor.close()



        conn.close()





# =============================================================================
# FUNCTION NAME : update_status
#
# PURPOSE :
# Updates approval request status.
#
# =============================================================================


def update_status(request_id, status):


    conn = db_connection()



    if conn is None:


        return




    cursor = None



    try:



        cursor = conn.cursor(buffered=True)



        cursor.execute("""


        UPDATE email_approvals


        SET status=%s


        WHERE id=%s



        """,

        (

            status,

            request_id

        )

        )



        conn.commit()



    except Error as err:



        print("\nStatus Update Error")

        print(err)



    finally:



        if cursor:


            cursor.close()



        conn.close()





# =============================================================================
# FUNCTION NAME : send_approved_email
#
# PURPOSE :
# Sends approved email through Gmail SMTP.
#
# =============================================================================


def send_approved_email(

        sender_email,

        app_password,

        receiver_email,

        subject,

        body

):


    try:



        email = EmailMessage()



        email["From"] = sender_email


        email["To"] = receiver_email


        email["Subject"] = subject



        email.set_content(body)



        server = smtplib.SMTP(

            "smtp.gmail.com",

            587

        )



        server.starttls()



        server.login(

            sender_email,

            app_password

        )



        server.send_message(email)



        server.quit()



        return True



    except Exception as err:



        print("\nEmail Sending Error")

        print(err)



        return False






# =============================================================================
# FUNCTION NAME : manager_panel
#
# PURPOSE :
# Manager approves or rejects email requests.
#
# =============================================================================


def manager_panel(manager_email, manager_password):


    print("\n===================================")

    print("        MANAGER APPROVAL PANEL")

    print("===================================")



    requests = view_pending_emails()



    if len(requests) == 0:


        return




    request_id = input(

        "\nEnter Email Request ID : "

    ).strip()



    if not request_id.isdigit():


        print("Invalid ID.")

        return




    email_data = get_email_request(request_id)



    if email_data is None:


        print("\nEmail Request Not Found.")

        return




    sender = email_data[0]

    receiver = email_data[1]

    subject = email_data[2]

    body = email_data[3]




    action = input(

        "\nApprove or Reject (A/R): "

    ).upper()




    if action == "A":



        result = send_approved_email(

            manager_email,

            manager_password,

            receiver,

            subject,

            body

        )



        if result:



            update_status(

                request_id,

                "Approved"

            )



            save_email_report(

                receiver,

                subject,

                "Success"

            )



            print("\nEmail Approved and Sent Successfully.")



        else:



            update_status(

                request_id,

                "Failed"

            )



            save_email_report(

                receiver,

                subject,

                "Failed"

            )





    elif action == "R":



        update_status(

            request_id,

            "Rejected"

        )



        print("\nEmail Request Rejected.")



    else:


        print("\nInvalid Option.")





# =============================================================================
# FUNCTION NAME : approval_workflow_menu
#
# PURPOSE :
# Main approval module menu.
#
# =============================================================================


def approval_workflow_menu(user_email=None, password=None):


    if user_email is None:


        user_email = input(

            "Enter Gmail ID : "

        )



        password = input(

            "Enter App Password : "

        )




    while True:



        print("\n===================================")

        print("      EMAIL APPROVAL WORKFLOW")

        print("===================================")

        print("1. Submit Email For Approval")

        print("2. Manager Approval Panel")

        print("3. Exit")

        print("===================================")



        choice = input(

            "Enter Choice : "

        )




        if choice == "1":


            request_email_approval(

                user_email

            )



        elif choice == "2":


            manager_panel(

                user_email,

                password

            )



        elif choice == "3":


            break



        else:


            print("Invalid Choice.")





# =============================================================================
# MAIN PROGRAM
# =============================================================================


if __name__ == "__main__":


    create_tables()



    approval_workflow_menu()