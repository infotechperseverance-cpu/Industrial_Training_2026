# =============================================================================
# FILE NAME   : dashboard.py
# PROJECT     : Email Automation System
# MODULE      : Email Analytics Dashboard
# DESCRIPTION : Displays email analytics from MySQL database.
# CALL FROM   : main.py
# =============================================================================

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
# DATABASE CONNECTION
# =============================================================================
def db_connection():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        return conn
    except Error as e:
        print("\nDatabase Connection Error :", e)
        return None


# =============================================================================
# CREATE REQUIRED TABLE
# =============================================================================
def create_table():
    conn = db_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS email_reports
    (
        id INT AUTO_INCREMENT PRIMARY KEY,
        recipient_email VARCHAR(255),
        subject VARCHAR(255),
        status VARCHAR(50),
        sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()


# =============================================================================
# CLASS : EmailAnalytics
# =============================================================================
class EmailAnalytics:

    def __init__(self):
        create_table()
        self.connection = db_connection()

        if self.connection is None:
            raise Exception("Database Connection Failed")

        self.cursor = self.connection.cursor()

    # -------------------------------------------------------------------------
    # SAFE COUNT FUNCTION
    # -------------------------------------------------------------------------
    def get_count(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result[0]
        except Error:
            return 0

    # -------------------------------------------------------------------------
    # DASHBOARD DISPLAY
    # -------------------------------------------------------------------------
    def dashboard(self):
        try:
            total = self.get_count("SELECT COUNT(*) FROM email_reports")

            success = self.get_count(
                """
                SELECT COUNT(*)
                FROM email_reports
                WHERE status='Success'
                """
            )

            failed = self.get_count(
                """
                SELECT COUNT(*)
                FROM email_reports
                WHERE status='Failed'
                """
            )

            today = self.get_count(
                """
                SELECT COUNT(*)
                FROM email_reports
                WHERE DATE(sent_date)=CURDATE()
                """
            )

            weekly = self.get_count(
                """
                SELECT COUNT(*)
                FROM email_reports
                WHERE YEARWEEK(sent_date,1) = YEARWEEK(CURDATE(),1)
                """
            )

            monthly = self.get_count(
                """
                SELECT COUNT(*)
                FROM email_reports
                WHERE MONTH(sent_date)=MONTH(CURDATE())
                AND YEAR(sent_date)=YEAR(CURDATE())
                """
            )

            contacts = self.get_count("SELECT COUNT(*) FROM contacts")
            drafts = self.get_count("SELECT COUNT(*) FROM drafts")
            reminders = self.get_count("SELECT COUNT(*) FROM email_reminders")

            if total == 0:
                rate = 0
            else:
                rate = (success / total) * 100

            print("\n================================================")
            print("             EMAIL ANALYTICS DASHBOARD")
            print("================================================")
            print(f"Total Emails Sent     : {total}")
            print(f"Successful Emails     : {success}")
            print(f"Failed Emails         : {failed}")
            print("-----------------------------------------------")
            print(f"Today's Emails        : {today}")
            print(f"This Week Emails      : {weekly}")
            print(f"This Month Emails     : {monthly}")
            print("-----------------------------------------------")
            print(f"Total Contacts        : {contacts}")
            print(f"Saved Drafts          : {drafts}")
            print(f"Email Reminders       : {reminders}")
            print("-----------------------------------------------")
            print(f"Success Rate          : {rate:.2f}%")
            print("================================================\n")

        except Exception as e:
            print("\nDashboard Error :", e)

    # -------------------------------------------------------------------------
    # CLOSE DATABASE
    # -------------------------------------------------------------------------
    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Error as e:
            print("Closing Error :", e)


# =============================================================================
# TEST RUN
# =============================================================================
if __name__ == "__main__":
    dashboard = EmailAnalytics()
    dashboard.dashboard()
    dashboard.close_connection()
