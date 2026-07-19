# FR-12: Email Analytics Dashboard
import mysql.connector
from datetime import datetime

# Database connection
conn = mysql.connector.connect(
host="localhost",
user="root",
password="root123",


)


class EmailAnalytics:

    def __init__(self):
        self.records = []

    def add_email(self, status):
        self.records.append({
            "date": datetime.now(),
            "status": status
        })

    def dashboard(self):
        total = len(self.records)
        success = sum(1 for r in self.records if r["status"] == "Success")
        failed = sum(1 for r in self.records if r["status"] == "Failed")

        today = datetime.now().date()
        current_week = datetime.now().isocalendar()[1]
        current_month = datetime.now().month

        daily = sum(1 for r in self.records
                    if r["date"].date() == today)

        weekly = sum(1 for r in self.records
                     if r["date"].isocalendar()[1] == current_week)

        monthly = sum(1 for r in self.records
                      if r["date"].month == current_month)

        print("\n========== EMAIL ANALYTICS DASHBOARD ==========")
        print(f"Total Emails Sent      : {total}")
        print(f"Successful Emails      : {success}")
        print(f"Failed Emails          : {failed}")
        print("-----------------------------------------------")
        print(f"Today's Emails         : {daily}")
        print(f"This Week Emails       : {weekly}")
        print(f"This Month Emails      : {monthly}")
        print("===============================================\n")


# Main Program

analytics = EmailAnalytics()

while True:
    print("1. Send Successful Email")
    print("2. Send Failed Email")
    print("3. View Email Analytics Dashboard")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        analytics.add_email("Success")
        print("Email sent successfully.\n")

    elif choice == "2":
        analytics.add_email("Failed")
        print("Email sending failed.\n")

    elif choice == "3":
        analytics.dashboard()

    elif choice == "4":
        print("Thank You!")
        break

    else:
        print("Invalid Choice!\n")