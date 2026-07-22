# =============================================================================
# FILE NAME : scheduler.py
#
# MODULE NAME : Smart Email Scheduler
#
# DESCRIPTION :
# This module schedules emails and automatically sends them
# at the selected date and time.
#
# DATABASE :
# email_automation
#
# TABLES :
# 1. scheduled_emails
# 2. email_reports
#
# =============================================================================


import smtplib
import ssl
import time
import threading


from datetime import datetime


from email.message import EmailMessage


import mysql.connector

from mysql.connector import Error





# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================


HOST = "localhost"

USER = "root"

PASSWORD = "root123"

DATABASE = "email_automation"





# =============================================================================
# DATABASE CONNECTION FUNCTION
#
# PURPOSE:
# Connects Python program with MySQL database.
#
# RETURNS:
# MySQL connection object
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
# CREATE REQUIRED TABLES
#
# Creates:
#
# 1. scheduled_emails
# 2. email_reports
#
# =============================================================================


def create_tables():


    conn = db_connection()



    if conn is None:


        return




    cursor = conn.cursor()



    try:



        # ---------------------------------------------------------
        # Scheduled Email Table
        # ---------------------------------------------------------


        cursor.execute("""


        CREATE TABLE IF NOT EXISTS scheduled_emails

        (

            id INT AUTO_INCREMENT PRIMARY KEY,


            recipient_email VARCHAR(255) NOT NULL,


            subject VARCHAR(255) NOT NULL,


            body TEXT NOT NULL,


            schedule_time DATETIME NOT NULL,


            status VARCHAR(50)
            DEFAULT 'Pending'


        )


        """)






        # ---------------------------------------------------------
        # Email Reports Table
        # ---------------------------------------------------------


        cursor.execute("""


        CREATE TABLE IF NOT EXISTS email_reports

        (

            id INT AUTO_INCREMENT PRIMARY KEY,


            recipient_email VARCHAR(255),


            subject VARCHAR(255),


            status VARCHAR(50),


            sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP


        )


        """)





        conn.commit()



        print("\nScheduler Database Ready.")




    except Error as err:


        print("\nTable Creation Error")

        print(err)



    finally:



        cursor.close()

        conn.close()







# =============================================================================
# SAVE EMAIL REPORT
#
# PURPOSE:
# Stores sent email status.
#
# STATUS:
# Success / Failed
#
# =============================================================================


def save_report(receiver, subject, status):


    conn = db_connection()



    if conn is None:


        return




    cursor = conn.cursor()



    try:



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

            receiver,

            subject,

            status

        )

        )



        conn.commit()




    except Error as err:



        print("\nReport Saving Error")

        print(err)




    finally:



        cursor.close()

        conn.close()

# =============================================================================
# SEND EMAIL FUNCTION
#
# PURPOSE:
# Sends scheduled email using Gmail SMTP.
#
# REQUIREMENT:
# Gmail App Password is required.
#
# =============================================================================


def send_email(

        sender_email,

        sender_password,

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





        context = ssl.create_default_context()



        server = smtplib.SMTP_SSL(

            "smtp.gmail.com",

            465,

            context=context

        )



        server.login(

            sender_email,

            sender_password

        )



        server.send_message(email)



        server.quit()



        print("\n===================================")

        print("EMAIL SENT SUCCESSFULLY")

        print("===================================")



        save_report(

            receiver_email,

            subject,

            "Success"

        )



        update_schedule_status(

            receiver_email,

            subject,

            "Completed"

        )



        return True





    except Exception as err:


        print("\n===================================")

        print("EMAIL SENDING FAILED")

        print("===================================")

        print(err)



        save_report(

            receiver_email,

            subject,

            "Failed"

        )



        update_schedule_status(

            receiver_email,

            subject,

            "Failed"

        )


        return False







# =============================================================================
# UPDATE SCHEDULE STATUS
#
# PURPOSE:
# Updates scheduled email status after sending.
#
# =============================================================================


def update_schedule_status(

        receiver,

        subject,

        status

):


    conn = db_connection()



    if conn is None:


        return



    cursor = conn.cursor()



    try:


        cursor.execute("""


        UPDATE scheduled_emails


        SET status=%s


        WHERE recipient_email=%s

        AND subject=%s


        """,

        (

            status,

            receiver,

            subject

        )

        )



        conn.commit()



    except Error as err:


        print("\nStatus Update Error")

        print(err)




    finally:


        cursor.close()

        conn.close()







# =============================================================================
# BACKGROUND SCHEDULER THREAD
#
# PURPOSE:
# Continuously checks scheduled time.
#
# When time arrives:
# Email is sent automatically.
#
# =============================================================================


def scheduler_worker(

        sender_email,

        sender_password,

        receiver_email,

        subject,

        body,

        schedule_datetime

):


    print("\nScheduler Started...")



    while True:



        current_time = datetime.now()



        if current_time >= schedule_datetime:



            print("\nScheduled time reached.")



            send_email(

                sender_email,

                sender_password,

                receiver_email,

                subject,

                body

            )



            break




        time.sleep(20)









# =============================================================================
# SCHEDULE EMAIL FUNCTION
#
# PURPOSE:
# Takes user input and stores scheduled email.
#
# =============================================================================


def schedule_email(

        sender_email,

        sender_password

):


    print("\n===================================")

    print("       SMART EMAIL SCHEDULER")

    print("===================================")





    receiver_email = input(

        "Enter Receiver Email : "

    ).strip()





    subject = input(

        "Enter Subject : "

    ).strip()




    body = input(

        "Enter Message : "

    ).strip()





    # -------------------------------------------------
    # DATE INPUT
    # -------------------------------------------------


    date = input(

        "\nEnter Schedule Date (YYYY-MM-DD) : "

    ).strip()





    # -------------------------------------------------
    # TIME INPUT
    # Example:
    # 05:30 PM
    # -------------------------------------------------


    time_input = input(

        "Enter Schedule Time (HH:MM AM/PM) : "

    ).strip().upper()





    try:



        schedule_datetime = datetime.strptime(

            date + " " + time_input,

            "%Y-%m-%d %I:%M %p"

        )



    except ValueError:



        print("\nInvalid Date or Time Format.")

        print("Example : 2026-07-25 05:30 PM")

        return






    if schedule_datetime <= datetime.now():



        print("\nSchedule time must be future time.")

        return






    # -------------------------------------------------
    # SAVE INTO DATABASE
    # -------------------------------------------------


    conn = db_connection()



    if conn is None:


        return




    cursor = conn.cursor()



    try:



        cursor.execute("""


        INSERT INTO scheduled_emails


        (

            recipient_email,

            subject,

            body,

            schedule_time,

            status

        )


        VALUES

        (

            %s,

            %s,

            %s,

            %s,

            %s

        )


        """,

        (

            receiver_email,

            subject,

            body,

            schedule_datetime,

            "Pending"

        )

        )



        conn.commit()




    except Error as err:


        print("\nSchedule Saving Error")

        print(err)

        return



    finally:


        cursor.close()

        conn.close()





    # -------------------------------------------------
    # START BACKGROUND THREAD
    # -------------------------------------------------



    thread = threading.Thread(

        target=scheduler_worker,

        args=(

            sender_email,

            sender_password,

            receiver_email,

            subject,

            body,

            schedule_datetime

        )

    )



    thread.daemon = True



    thread.start()





    print("\nEmail Scheduled Successfully.")

    print(

        "Scheduled Time :",

        schedule_datetime

    )

# =============================================================================
# FUNCTION NAME : view_schedule
#
# PURPOSE :
# Displays all scheduled emails.
#
# =============================================================================


def view_schedule():

    conn = db_connection()

    if conn is None:
        return


    cursor = None


    try:

        cursor = conn.cursor()


        cursor.execute(

            """
            SELECT

                id,
                recipient_email,
                subject,
                schedule_time,
                status

            FROM scheduled_emails

            ORDER BY schedule_time

            """

        )


        records = cursor.fetchall()



        print("\n==========================================")
        print("          SCHEDULED EMAIL LIST")
        print("==========================================")



        if len(records) == 0:

            print("No Scheduled Emails Found.")



        else:


            for row in records:


                print("------------------------------------------")

                print("ID             :", row[0])

                print("Receiver Email :", row[1])

                print("Subject        :", row[2])

                print("Schedule Time  :", row[3])

                print("Status         :", row[4])



    except Error as err:


        print("\nUnable To Fetch Schedule")

        print(err)



    finally:


        if cursor:

            cursor.close()


        conn.close()







# =============================================================================
# FUNCTION NAME : scheduler_menu
#
# PURPOSE :
# Main menu of Email Scheduler.
#
# =============================================================================

def scheduler_menu(sender_email=None, sender_password=None):

    create_tables()

    while True:

        print("\n======================================")
        print("          SMART EMAIL SCHEDULER")
        print("======================================")
        print("1. Schedule New Email")
        print("2. View Scheduled Emails")
        print("3. Exit")
        print("======================================")

        choice = input("Enter Choice : ").strip()

        if choice == "1":

            if sender_email is None or sender_password is None:

                sender_email = input("\nEnter Gmail ID : ").strip()

                sender_password = input(
                    "Enter Gmail App Password : "
                ).strip()

            schedule_email(

                sender_email,

                sender_password

            )

        elif choice == "2":

            view_schedule()

        elif choice == "3":

            print("\nExiting Scheduler...")

            break

        else:

            print("\nInvalid Choice.")



# =============================================================================
# MAIN PROGRAM
# =============================================================================


if __name__ == "__main__":



    create_tables()



    print("\n================================")

    print("       EMAIL AUTOMATION LOGIN")

    print("================================")



    sender_email = input(

        "Enter Gmail ID : "

    ).strip()



    sender_password = input(

        "Enter Gmail App Password : "

    ).strip()




    scheduler_menu(

        sender_email,

        sender_password

    )