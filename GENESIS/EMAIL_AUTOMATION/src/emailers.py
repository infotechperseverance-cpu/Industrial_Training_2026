# =============================================================================
# FILE NAME : emailers.py
#
# PROJECT : Email Automation System
#
# DESCRIPTION :
# This module manages Email Reminders.
#
# FEATURES :
# 1. Add Reminder
# 2. View Reminder
# 3. Update Reminder Status
# 4. Delete Reminder
# 5. Automatic Reminder Notification
#
# DATABASE :
# email_automation
#
# TABLE :
# email_reminders
#
# AUTHOR : Mansi More
# =============================================================================


# =============================================================================
# IMPORT MODULES
# =============================================================================

import re
import time
import threading
import mysql.connector

from datetime import datetime
from mysql.connector import Error

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False


# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

HOST = "localhost"
USER = "root"
PASSWORD = "root123"          # Change according to your MySQL Password
DATABASE = "email_automation"


# =============================================================================
# FUNCTION NAME : db_connection
#
# PURPOSE :
# Creates connection with MySQL database.
#
# RETURNS :
# Database Connection Object
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

        print("\n======================================")
        print("DATABASE CONNECTION ERROR")
        print("======================================")
        print(err)

        return None


# =============================================================================
# FUNCTION NAME : create_table
#
# PURPOSE :
# Creates email_reminders table if it does not exist.
# =============================================================================

def create_table():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        query = """

        CREATE TABLE IF NOT EXISTS email_reminders
        (

            id INT AUTO_INCREMENT PRIMARY KEY,

            recipient_email VARCHAR(255) NOT NULL,

            subject VARCHAR(255) NOT NULL,

            message TEXT NOT NULL,

            reminder_date DATETIME NOT NULL,

            status VARCHAR(30)
            DEFAULT 'Pending'

        )

        """

        cursor.execute(query)

        conn.commit()

    except Error as err:

        print("\nTable Creation Error")
        print(err)

    finally:

        if cursor:

            cursor.close()

        conn.close()


# =============================================================================
# FUNCTION NAME : check_email
#
# PURPOSE :
# Validates Gmail Address.
#
# RETURNS :
# True / False
# =============================================================================

def check_email(email):

    pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'

    return bool(re.fullmatch(pattern, email))


# =============================================================================
# FUNCTION NAME : show_notification
#
# PURPOSE :
# Displays desktop popup notification.
#
# INPUT :
# Subject
# Message
#
# OUTPUT :
# Windows Desktop Notification
# =============================================================================

def show_notification(subject, message):

    if PLYER_AVAILABLE:

        try:

            notification.notify(

                title="Email Reminder",

                message=f"{subject}\n\n{message}",

                timeout=10

            )

        except Exception:

            print("\nNotification Error.")

    else:

        print("\n======================================")
        print("          EMAIL REMINDER")
        print("======================================")
        print("Subject :", subject)
        print("Message :", message)
        print("======================================")


# =============================================================================
# FUNCTION NAME : check_due_reminders
#
# PURPOSE :
# Checks database for reminders whose reminder time
# has arrived.
#
# NOTE :
# Called continuously by background thread.
#
# OUTPUT :
# Shows notification and updates reminder status.
#
# Remaining logic will be completed in Part 5.
# =============================================================================

def check_due_reminders():

    pass


# =============================================================================
# BACKGROUND THREAD OBJECT
# =============================================================================

reminder_thread = None

# =============================================================================
# FUNCTION NAME : add_reminder
#
# PURPOSE :
# Adds a new email reminder to the database.
#
# INPUT :
# Recipient Email
# Subject
# Message
# Reminder Date & Time
#
# OUTPUT :
# Saves reminder into email_reminders table.
# =============================================================================

def add_reminder():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        print("\n========================================")
        print("          ADD EMAIL REMINDER")
        print("========================================")

        # ---------------------------------------------------------
        # Recipient Email
        # ---------------------------------------------------------

        while True:

            receiver = input("Recipient Gmail : ").strip()

            if receiver == "":

                print("Recipient Email cannot be empty.")

                continue

            if not check_email(receiver):

                print("Please enter a valid Gmail Address.")

                continue

            break

        # ---------------------------------------------------------
        # Subject
        # ---------------------------------------------------------

        while True:

            subject = input("Subject : ").strip()

            if subject == "":

                print("Subject cannot be empty.")

                continue

            break

        # ---------------------------------------------------------
        # Message
        # ---------------------------------------------------------

        while True:

            message = input("Message : ").strip()

            if message == "":

                print("Message cannot be empty.")

                continue

            break

        # ---------------------------------------------------------
        # Reminder Date & Time
        # ---------------------------------------------------------

        while True:

            reminder = input(
                "Reminder Date (YYYY-MM-DD HH:MM:SS) : "
            ).strip()

            try:

                reminder_datetime = datetime.strptime(
                    reminder,
                    "%Y-%m-%d %H:%M:%S"
                )

                if reminder_datetime <= datetime.now():

                    print("Reminder must be a future date and time.")

                    continue

                break

            except ValueError:

                print("Invalid Date Format.")
                print("Example : 2026-08-10 14:30:00")

        # ---------------------------------------------------------
        # Save Reminder
        # ---------------------------------------------------------

        query = """

        INSERT INTO email_reminders
        (

            recipient_email,

            subject,

            message,

            reminder_date,

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

        """

        cursor.execute(

            query,

            (

                receiver,

                subject,

                message,

                reminder_datetime,

                "Pending"

            )

        )

        conn.commit()

        print("\n========================================")
        print("Reminder Added Successfully.")
        print("Status : Pending")
        print("========================================")

    except Error as err:

        print("\nUnable to Add Reminder.")
        print(err)

    finally:

        if cursor:

            cursor.close()

        conn.close()

# =============================================================================
# FUNCTION NAME : view_reminders
#
# PURPOSE :
# Displays all reminders stored in the database.
#
# INPUT :
# None
#
# OUTPUT :
# Prints reminder details in ascending order of reminder date.
# =============================================================================

def view_reminders():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        query = """

        SELECT

            id,

            recipient_email,

            subject,

            message,

            reminder_date,

            status

        FROM email_reminders

        ORDER BY reminder_date ASC

        """

        cursor.execute(query)

        records = cursor.fetchall()

        print("\n==============================================")
        print("             EMAIL REMINDERS")
        print("==============================================")

        if len(records) == 0:

            print("No Reminder Found.")
            return

        for row in records:

            print("----------------------------------------------")
            print("Reminder ID     :", row[0])
            print("Recipient Email :", row[1])
            print("Subject         :", row[2])
            print("Message         :", row[3])

            if isinstance(row[4], datetime):

                print(
                    "Reminder Date   :",
                    row[4].strftime("%Y-%m-%d %H:%M:%S")
                )

            else:

                print("Reminder Date   :", row[4])

            print("Status          :", row[5])

        print("----------------------------------------------")
        print("Total Reminders :", len(records))
        print("==============================================")

    except Error as err:

        print("\nUnable to Fetch Reminders.")
        print(err)

    finally:

        if cursor:

            cursor.close()

        conn.close()

# =============================================================================
# FUNCTION NAME : update_status
#
# PURPOSE :
# Updates reminder status.
#
# INPUT :
# Reminder ID
# New Status
#
# OUTPUT :
# Updates reminder status in database.
# =============================================================================

def update_status():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        print("\n========================================")
        print("      UPDATE REMINDER STATUS")
        print("========================================")

        reminder_id = input("Enter Reminder ID : ").strip()

        if not reminder_id.isdigit():

            print("Invalid Reminder ID.")

            return

        cursor.execute(

            "SELECT id FROM email_reminders WHERE id=%s",

            (reminder_id,)

        )

        if cursor.fetchone() is None:

            print("Reminder ID not found.")

            return

        while True:

            status = input(
                "Enter Status (Pending/Completed) : "
            ).strip().title()

            if status in ("Pending", "Completed"):

                break

            print("Invalid Status.")

        cursor.execute(

            """

            UPDATE email_reminders

            SET status=%s

            WHERE id=%s

            """,

            (

                status,

                reminder_id

            )

        )

        conn.commit()

        print("\nReminder Status Updated Successfully.")

    except Error as err:

        print("\nUnable to Update Reminder.")
        print(err)

    finally:

        if cursor:

            cursor.close()

        conn.close()


# =============================================================================
# FUNCTION NAME : delete_reminder
#
# PURPOSE :
# Deletes a reminder from the database.
#
# INPUT :
# Reminder ID
#
# OUTPUT :
# Deletes reminder permanently.
# =============================================================================

def delete_reminder():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        print("\n========================================")
        print("         DELETE REMINDER")
        print("========================================")

        reminder_id = input("Enter Reminder ID : ").strip()

        if not reminder_id.isdigit():

            print("Invalid Reminder ID.")

            return

        cursor.execute(

            "SELECT id FROM email_reminders WHERE id=%s",

            (reminder_id,)

        )

        if cursor.fetchone() is None:

            print("Reminder ID not found.")

            return

        confirm = input(
            "Are you sure? (Y/N) : "
        ).strip().upper()

        if confirm != "Y":

            print("Delete Cancelled.")

            return

        cursor.execute(

            """

            DELETE FROM email_reminders

            WHERE id=%s

            """,

            (reminder_id,)

        )

        conn.commit()

        print("\nReminder Deleted Successfully.")

    except Error as err:

        print("\nUnable to Delete Reminder.")
        print(err)

    finally:

        if cursor:

            cursor.close()

        conn.close()

# =============================================================================
# FUNCTION NAME : check_due_reminders
#
# PURPOSE :
# Continuously checks the database for reminders whose
# reminder time has arrived.
#
# OUTPUT :
# Shows desktop notification and automatically updates
# reminder status from Pending to Completed.
# =============================================================================

def check_due_reminders():

    while True:

        conn = db_connection()

        if conn is not None:

            cursor = None

            try:

                cursor = conn.cursor(buffered=True)

                query = """

                SELECT

                    id,
                    subject,
                    message

                FROM email_reminders

                WHERE

                    reminder_date <= NOW()

                    AND status='Pending'

                """

                cursor.execute(query)

                reminders = cursor.fetchall()

                for reminder in reminders:

                    reminder_id = reminder[0]
                    subject = reminder[1]
                    message = reminder[2]

                    # ----------------------------------------
                    # Show Notification
                    # ----------------------------------------

                    show_notification(subject, message)

                    # ----------------------------------------
                    # Update Status
                    # ----------------------------------------

                    cursor.execute(

                        """

                        UPDATE email_reminders

                        SET status='Completed'

                        WHERE id=%s

                        """,

                        (reminder_id,)

                    )

                    conn.commit()

            except Error as err:

                print("\nReminder Thread Error")
                print(err)

            finally:

                if cursor:

                    cursor.close()

                conn.close()

        # --------------------------------------------
        # Check every 10 seconds
        # --------------------------------------------

        time.sleep(10)


# =============================================================================
# FUNCTION NAME : start_reminder_thread
#
# PURPOSE :
# Starts background reminder thread only once.
# =============================================================================

def start_reminder_thread():

    global reminder_thread

    if reminder_thread is None:

        reminder_thread = threading.Thread(

            target=check_due_reminders,

            daemon=True

        )

        reminder_thread.start()


# =============================================================================
# FUNCTION NAME : reminder_menu
#
# PURPOSE :
# Displays Reminder Menu.
# =============================================================================

def reminder_menu():

    create_table()

    start_reminder_thread()

    while True:

        print("\n======================================")
        print("        EMAIL REMINDER SYSTEM")
        print("======================================")
        print("1. Add Reminder")
        print("2. View Reminders")
        print("3. Update Reminder Status")
        print("4. Delete Reminder")
        print("5. Exit")
        print("======================================")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":

            add_reminder()

        elif choice == "2":

            view_reminders()

        elif choice == "3":

            update_status()

        elif choice == "4":

            delete_reminder()

        elif choice == "5":

            print("\nReturning to Dashboard...")

            break

        else:

            print("\nInvalid Choice.")


# =============================================================================
# MAIN PROGRAM
# =============================================================================

if __name__ == "__main__":

    reminder_menu()