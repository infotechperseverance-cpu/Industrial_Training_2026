# =============================================================================
# FILE NAME   : draft_management.py
# MODULE NAME : Draft Management System
# DESCRIPTION : This module manages email drafts.
# FEATURES    :
#   1. Create Draft
#   2. Save AI Generated Email Draft
#   3. View Drafts
#   4. Update Draft
#   5. Delete Draft
# DATABASE    : email_automation
# TABLE       : drafts
# NOTE        : Handles draft operations using AIEmailWriter and MySQL.
# =============================================================================

from datetime import datetime
import mysql.connector
from mysql.connector import Error
from ai_email import AIEmailWriter


# =============================================================================
# DATABASE CONNECTION
# =============================================================================
def db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="email_automation"
        )
        return connection

    except Error as e:
        print("\n======================================")
        print("DATABASE CONNECTION ERROR")
        print("======================================")
        print(e)
        return None


# =============================================================================
# CREATE TABLE
# =============================================================================
def create_table():
    conn = db_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS drafts
    (
        id INT AUTO_INCREMENT PRIMARY KEY,
        receiver_email VARCHAR(255) NOT NULL,
        subject VARCHAR(255) NOT NULL,
        message TEXT NOT NULL,
        created_on DATETIME NOT NULL
    )
    """

    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()


# =============================================================================
# CLASS NAME : DraftManagement
# PURPOSE    : Handles all draft operations.
# =============================================================================
class DraftManagement:

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================
    def __init__(self):
        create_table()
        self.connection = db_connection()

        if self.connection:
            self.cursor = self.connection.cursor()
        else:
            raise Exception("Database Connection Failed")

    # =========================================================================
    # SAVE DRAFT
    # =========================================================================
    def save_draft(self, reciever_email, subject, body):
        try:
            query = """
            INSERT INTO drafts
            (receiver_email, subject, message, created_on)
            VALUES(%s,%s,%s,%s)
            """

            self.cursor.execute(
                query,
                (
                    reciever_email,
                    subject,
                    body,
                    datetime.now()
                )
            )

            self.connection.commit()
            print("\nDraft Saved Successfully.")

        except Error as e:
            print("\nError Saving Draft :", e)

    # =========================================================================
    # CREATE DRAFT
    # =========================================================================
    def create_draft(self):
        print("\n================================")
        print("        CREATE EMAIL DRAFT")
        print("================================")

        receiver = input("Receiver Email : ").strip()

        print("\nSelect Draft Type")
        print("1. Manual Draft")
        print("2. AI Generated Draft")

        choice = input("\nEnter Choice : ").strip()

        # MANUAL DRAFT
        if choice == "1":
            subject = input("\nSubject : ").strip()

            print("\nEnter Email Body")
            print("Press ENTER twice to finish.\n")

            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            body = "\n".join(lines)

        # AI GENERATED DRAFT
        elif choice == "2":
            topic = input("\nEnter Email Topic : ").strip()

            print("\nSelect Email Tone")
            print("1. Professional")
            print("2. Friendly")
            print("3. Formal")
            print("4. Apology")
            print("5. Thank You")
            print("6. Request")
            print("7. Invitation")

            tone_choice = input("\nEnter Choice : ").strip()
            details = input("\nEnter Additional Details : ").strip()

            ai = AIEmailWriter()
            subject, body = ai.generate_email(
                topic,
                tone_choice,
                details
            )

            if subject == "Error":
                print(body)
                return

            print("\n================================")
            print("      AI GENERATED DRAFT")
            print("================================")
            print("\nSubject :")
            print(subject)
            print("\nBody :")
            print(body)

            confirm = input("\nSave this draft? (Y/N) : ").strip().upper()
            if confirm != "Y":
                print("\nDraft Not Saved.")
                return

        else:
            print("\nInvalid Choice.")
            return

        # VALIDATION
        if subject == "" or body == "":
            print("\nSubject and Body cannot be empty.")
            return

        self.save_draft(receiver, subject, body)

    # =========================================================================
    # VIEW DRAFTS
    # =========================================================================
    def view_drafts(self):
        try:
            query = """
            SELECT 
            id,
            receiver_email,
            subject,
            created_on
            FROM drafts
            ORDER BY created_on DESC
            """

            self.cursor.execute(query)
            records = self.cursor.fetchall()

            print("\n================================")
            print("          SAVED DRAFTS")
            print("================================")

            if len(records) == 0:
                print("No Drafts Available")
                return

            print(
                "{:<8}{:<30}{:<30}{:<25}".format(
                    "ID", "Receiver", "Subject", "Created Date"
                )
            )
            print("-" * 95)

            for row in records:
                print(
                    "{:<8}{:<30}{:<30}{:<25}".format(
                        row[0], row[1], row[2], str(row[3])
                    )
                )

        except Error as e:
            print("\nDatabase Error :", e)

    # =========================================================================
    # UPDATE DRAFT
    # =========================================================================
    def update_draft(self):
        self.view_drafts()

        draft_id = input("\nEnter Draft ID to Update : ")
        subject = input("New Subject : ")
        print("New Body : ")
        body = input()

        try:
            query = """
            UPDATE drafts
            SET subject=%s,
            message=%s
            WHERE id=%s
            """

            self.cursor.execute(query, (subject, body, draft_id))
            self.connection.commit()

            print("\nDraft Updated Successfully.")

        except Error as e:
            print("\nUpdate Error :", e)

    # =========================================================================
    # DELETE DRAFT
    # =========================================================================
    def delete_draft(self):
        self.view_drafts()

        draft_id = input("\nEnter Draft ID to Delete : ")

        try:
            query = """
            DELETE FROM drafts
            WHERE id=%s
            """

            self.cursor.execute(query, (draft_id,))
            self.connection.commit()

            print("\nDraft Deleted Successfully.")

        except Error as e:
            print("\nDelete Error :", e)

    # =========================================================================
    # CLOSE DATABASE CONNECTION
    # =========================================================================
    def close_connection(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()


# =============================================================================
# MENU SYSTEM
# =============================================================================
def draft_menu():
    draft = DraftManagement()

    while True:
        print("\n====================================")
        print("        DRAFT MANAGEMENT SYSTEM")
        print("====================================")
        print("1. Create Draft")
        print("2. View Drafts")
        print("3. Update Draft")
        print("4. Delete Draft")
        print("5. Back")
        print("====================================")

        choice = input("Enter Choice : ")

        if choice == "1":
            draft.create_draft()

        elif choice == "2":
            draft.view_drafts()

        elif choice == "3":
            draft.update_draft()

        elif choice == "4":
            draft.delete_draft()

        elif choice == "5":
            draft.close_connection()
            print("\nReturning to Main Menu...")
            break

        else:
            print("\nInvalid Choice")


# =============================================================================
# MAIN PROGRAM
# =============================================================================
if __name__ == "__main__":
    draft_menu()
