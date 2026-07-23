# =============================================================================
# FILE NAME : bulk_email.py
#
# PROJECT : EMAIL AUTOMATION SYSTEM
#
# DESCRIPTION :
# This module sends a bulk email to all contacts belonging
# to a selected contact group.
#
# DATABASE :
# email_automation
#
# TABLES USED :
# 1. contact_groups
# 2. contacts
#
# AUTHOR : Mansi More
# =============================================================================

# =============================================================================
# IMPORT MODULES
# =============================================================================

import msvcrt
import smtplib
import ssl
import sys
import sys
from ai_email import AIEmailWriter

from login import get_password
import mysql.connector
import getpass

from email.message import EmailMessage
from mysql.connector import Error
from datetime import datetime

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

HOST = "localhost"
USER = "root"
PASSWORD = "root123"
DATABASE = "email_automation"

# =============================================================================
# CLASS : BulkEmail
# =============================================================================

class BulkEmail:

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(self):

        self.connection = None
        self.cursor = None

        self.connect_database()

    # =========================================================================
    # FUNCTION : connect_database()
    #
    # PURPOSE :
    # Connect with MySQL database.
    # =========================================================================

    def connect_database(self):

        try:

            self.connection = mysql.connector.connect(

                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE

            )

            if self.connection.is_connected():

                self.cursor = self.connection.cursor(buffered=True)

        except Error as err:

            print("\n===================================")
            print("DATABASE CONNECTION ERROR")
            print("===================================")
            print(err)

    # =========================================================================
    # FUNCTION : show_groups()
    #
    # PURPOSE :
    # Display all available contact groups.
    # =========================================================================

    def show_groups(self):

        try:

            self.cursor.execute("""

                SELECT
                    group_id,
                    group_name

                FROM contact_groups

                ORDER BY group_name

            """)

            groups = self.cursor.fetchall()

            if len(groups) == 0:

                print("\nNo Contact Groups Found.")

                return []

            print("\n===================================")
            print("       AVAILABLE GROUPS")
            print("===================================")

            for group in groups:

                print(f"{group[0]}. {group[1]}")

            print("===================================")

            return groups

        except Error as err:

            print("\nUnable To Fetch Groups")
            print(err)

            return []

    # =========================================================================
    # FUNCTION : get_group_contacts()
    #
    # PURPOSE :
    # Returns all contacts belonging to selected group.
    # =========================================================================

    def get_group_contacts(self, group_id):

        try:

            self.cursor.execute("""

                SELECT

                    name,
                    email

                FROM contacts

                WHERE group_id=%s

                ORDER BY name

            """, (group_id,))

            contacts = self.cursor.fetchall()

            return contacts

        except Error as err:

            print("\nUnable To Fetch Contacts")
            print(err)

            return []

    # =========================================================================
    # FUNCTION : display_contacts()
    #
    # PURPOSE :
    # Display contacts before sending emails.
    # =========================================================================

    def display_contacts(self, contacts):

        print("\n===================================")
        print("        CONTACT LIST")
        print("===================================")

        if len(contacts) == 0:

            print("No Contacts Available.")

            return

        count = 1

        for name, email in contacts:

            print(f"{count}. {name}")
            print(f"   {email}")
            print("-----------------------------------")

            count += 1

    # =========================================================================
    # FUNCTION : check_email()
    #
    # PURPOSE :
    # Simple email validation.
    # =========================================================================

    def check_email(self, email):

        if "@" not in email:

            return False

        if "." not in email:

            return False

        return True

    # =============================================================================
    # FUNCTION : get_password()
    # =============================================================================

    def get_password(prompt="Enter Gmail App Password : "):

        print(prompt, end="", flush=True)

        password = ""

        while True:

            ch = msvcrt.getch()

            # ENTER KEY
            if ch in (b'\r', b'\n'):

                print()
                break

            # BACKSPACE
            elif ch == b'\x08':

                if len(password) > 0:

                    password = password[:-1]

                    sys.stdout.write("\b \b")
                    sys.stdout.flush()

            # Ignore Arrow Keys / Function Keys
            elif ch in (b'\x00', b'\xe0'):

                msvcrt.getch()

            else:

                try:

                    character = ch.decode("utf-8")

                    password += character

                    sys.stdout.write("*")
                    sys.stdout.flush()

                except:

                    pass

        return password
    
    # =========================================================================
    # FUNCTION : send_bulk_email()
    #
    # PURPOSE :
    # Sends email to every contact of the selected group.
    # =========================================================================

    def send_bulk_email(self):

        # -------------------------------------------------------------
        # Show Available Groups
        # -------------------------------------------------------------

        groups = self.show_groups()

        if len(groups) == 0:

            return

        # -------------------------------------------------------------
        # Select Group
        # -------------------------------------------------------------

        group_id = input("\nEnter Group ID : ").strip()

        if not group_id.isdigit():

            print("\nInvalid Group ID.")

            return

        group_found = False
        group_name = ""

        for group in groups:

            if int(group_id) == group[0]:

                group_found = True
                group_name = group[1]
                break

        if not group_found:

            print("\nGroup Not Found.")

            return

        # -------------------------------------------------------------
        # Get Contacts
        # -------------------------------------------------------------

        contacts = self.get_group_contacts(group_id)

        if len(contacts) == 0:

            print("\nNo Contacts Found In This Group.")

            return

        print(f"\nSelected Group : {group_name}")

        self.display_contacts(contacts)

        # -------------------------------------------------------------
        # Sender Details
        # -------------------------------------------------------------

        print("\n===================================")
        print("         SENDER DETAILS")
        print("===================================")

        sender_email = input("Enter Gmail ID : ").strip()

        password = get_password("Enter Gmail App Password : ")

        password = password.replace(" ", "")

        if password == "":
            print("\nPassword cannot be empty.")
            return
        # -------------------------------------------------------------
        # Email Subject
        # -------------------------------------------------------------

        subject = input("\nEnter Email Subject : ").strip()

        # -------------------------------------------------------------
        # Email Generation Method
        # -------------------------------------------------------------

        print("\n===================================")
        print("      EMAIL GENERATION")
        print("===================================")
        print("1. Manual Email")
        print("2. AI Generated Email")
        print("===================================")

        choice = input("Enter Choice : ").strip()

        # =============================================================
        # MANUAL EMAIL
        # =============================================================

        if choice == "1":

            print("\nEnter Email Message")
            print("Press ENTER twice to finish.\n")

            lines = []

            while True:

                line = input()

                if line == "":
                    break

                lines.append(line)

            body = "\n".join(lines)

        # =============================================================
        # AI EMAIL
        # =============================================================

        elif choice == "2":

            print("\n===================================")
            print("      AI EMAIL GENERATOR")
            print("===================================")

            topic = input("Enter Email Topic : ")

            tone = input("Enter Email Tone : ")

            details = input("Enter Additional Details : ")

            ai = AIEmailWriter()

            ai_subject, body = ai.generate_email(
                topic,
                tone,
                details
            )

            # Use AI generated subject if available
            if ai_subject != "Error":
                subject = ai_subject

            print("\n===================================")
            print("AI EMAIL GENERATED")
            print("===================================")

            print("\nSubject :", subject)

            print("\nBody:\n")
            print(body)

        else:

            print("\nInvalid Choice.")
            return

        # -------------------------------------------------------------
        # SMTP Login
        # -------------------------------------------------------------

        try:

            context = ssl.create_default_context()

            server = smtplib.SMTP("smtp.gmail.com", 587)

            server.ehlo()

            server.starttls(context=context)

            server.ehlo()

            server.login(sender_email, password)

        except smtplib.SMTPAuthenticationError:

            print("\n===================================")
            print("SMTP LOGIN FAILED")
            print("===================================")
            print("Invalid Gmail ID or App Password.")
            print("Make sure:")
            print("1. Gmail 2-Step Verification is ON")
            print("2. You are using a Google App Password")
            print("3. The App Password is entered without spaces")
            return

        except Exception as e:

            print("\nSMTP Error")
            print(e)
            return

        # -------------------------------------------------------------
        # Send Emails
        # -------------------------------------------------------------

        print("\n===================================")
        print("        SENDING EMAILS")
        print("===================================\n")

        success = 0
        failed = 0

        for name, email in contacts:

            if not self.check_email(email):

                print(f"Invalid Email : {email}")

                failed += 1

                continue

            try:

                message = EmailMessage()

                message["From"] = sender_email
                message["To"] = email
                message["Subject"] = subject

                message.set_content(

                    f"""Hello {name},

                {body}

                Regards,
                {sender_email}
                """
                )

                server.send_message(message)

                print(f"✓ Email Sent To : {name} ({email})")

                success += 1

            except Exception as e:

                print(f"✗ Failed : {email}")

                failed += 1

        server.quit()

        # -------------------------------------------------------------
        # Summary
        # -------------------------------------------------------------

        print("\n===================================")
        print("      BULK EMAIL SUMMARY")
        print("===================================")

        print("Selected Group :", group_name)
        print("Total Contacts :", len(contacts))
        print("Success        :", success)
        print("Failed         :", failed)
        print("Completed On   :", datetime.now())

        print("===================================")

    # =========================================================================
    # FUNCTION : close_connection()
    #
    # PURPOSE :
    # Close MySQL database connection.
    # =========================================================================

    def close_connection(self):

        try:

            if self.cursor:

                self.cursor.close()

            if self.connection:

                if self.connection.is_connected():

                    self.connection.close()

        except Error as err:

            print("\nDatabase Close Error")
            print(err)

    # =========================================================================
    # FUNCTION : run()
    #
    # PURPOSE :
    # Display Bulk Email Menu.
    # =========================================================================

    def run(self):

        while True:

            print("\n===================================")
            print("         BULK EMAIL MENU")
            print("===================================")
            print("1. Send Bulk Email")
            print("2. Exit")
            print("===================================")

            choice = input("Enter Choice : ").strip()

            if choice == "1":

                self.send_bulk_email()

            elif choice == "2":

                print("\nReturning to Dashboard...")

                break

            else:

                print("\nInvalid Choice.")

# =============================================================================
# PROGRAM START
# =============================================================================

if __name__ == "__main__":

    obj = BulkEmail()

    obj.run()