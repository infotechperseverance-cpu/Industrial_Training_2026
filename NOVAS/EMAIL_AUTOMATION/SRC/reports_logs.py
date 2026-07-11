import json
import csv
from datetime import datetime
from voice import speak

EMAIL_FILE = "email_records.json"
REPORT_FILE = "email_report.csv"
LOG_FILE = "logs.csv"


# ---------------- Load Email Records ----------------

def load_email_records():
    try:
        with open(EMAIL_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# ---------------- Generate Report ----------------

'''

@Function Name: generate_reports
@Description  : This function checks the total, 
                completed, pending, and failed 
                emails from email_records.json 
                and stores the report in 
                email_reports.json.
@InputParam   : None
@OutputParam  : report

'''

def generate_report():

    records = load_email_records()

    if not records:
        return None

    total = len(records)
    completed = 0
    pending = 0
    failed = 0

    for email in records:

        status = email["status"].lower()

        if status == "completed":
            completed += 1

        elif status == "pending":
            pending += 1

        elif status == "failed":
            failed += 1

    success_rate = 0

    if total > 0:
        success_rate = (completed / total) * 100

    report = {
        "Total Emails": total,
        "Completed Emails": completed,
        "Pending Emails": pending,
        "Failed Emails": failed,
        "Success Rate": round(success_rate, 2)
    }

    return report


# ---------------- View Report ----------------

'''

@Function Name: view_report_summary
@Description  : This function for view reports from
                email_reports.json.
@InputParam   : NONE
@OutputParam  : NONE

'''


def view_report_summary():

    report = generate_report()

    if report is None:
        print("\nNo email records found.")
        return

    print("\n========================================")
    print("        EMAIL REPORT SUMMARY")
    print("========================================")
    print(f"Total Emails      : {report['Total Emails']}")
    print(f"Completed Emails  : {report['Completed Emails']}")
    print(f"Pending Emails    : {report['Pending Emails']}")
    print(f"Failed Emails     : {report['Failed Emails']}")
    print(f"Success Rate      : {report['Success Rate']} %")
    print("========================================")


# ---------------- Export Report ----------------

'''

@Function Name: export_report_to_csv
@Description  : This function store report summary
                in email_report.json
@InputParam   : None
@OutputParam  : report

'''


def export_report_to_csv():

    report = generate_report()

    if report is None:
        print("No email records found.")
        return

    with open(REPORT_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Report", "Count"])

        writer.writerow(["Total Emails", report["Total Emails"]])
        writer.writerow(["Completed Emails", report["Completed Emails"]])
        writer.writerow(["Pending Emails", report["Pending Emails"]])
        writer.writerow(["Failed Emails", report["Failed Emails"]])
        writer.writerow(["Success Rate", str(report["Success Rate"]) + " %"])

    print("\nReport exported successfully.")


# ---------------- Save Log ----------------

'''

@Function Name: save_log
@Description  : This function save logs in logs.csv
@InputParam   : None
@OutputParam  : report

'''


def save_log(email_id, action):

    try:
        with open(LOG_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)

            if len(rows) <= 1:
                log_id = 1
            else:
                log_id = len(rows)

    except FileNotFoundError:
        log_id = 1

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow([
                "Log ID",
                "Email ID",
                "Action",
                "Date",
                "Time"
            ])

        writer.writerow([
            log_id,
            email_id,
            action,
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%I:%M:%S %p")
        ])


# ---------------- View Logs ----------------

'''

@Function Name: view_logs
@Description  : This function view logs from logs.csv
@InputParam   : None
@OutputParam  : report

'''


def view_logs():

    try:

        with open(LOG_FILE, "r", newline="") as file:

            reader = csv.DictReader(file)

            records = list(reader)

            if not records:
                print("\nNo logs available.")
                return

            print("\n==============================================")
            print("               EMAIL LOGS")
            print("==============================================")

            for log in records:

                print(f"Log ID   : {log['Log ID']}")
                print(f"Email ID : {log['Email ID']}")
                print(f"Action   : {log['Action']}")
                print(f"Date     : {log['Date']}")
                print(f"Time     : {log['Time']}")
                print("----------------------------------------------")

    except FileNotFoundError:
        print("\nNo logs found.")


# ---------------- Reports & Logs Menu ----------------

def reports_logs_menu():

    while True:

        speak("\n---------- REPORTS & LOGS -----------")
        print("\nREPORTS & LOGS")
        print("1. View Report Summary")
        print("2. Export Report to CSV")
        print("3. View Logs")
        print("4. Back")

        choice = input("\nEnter Choice: ")

        if choice == "1":
            view_report_summary()

        elif choice == "2":
            export_report_to_csv()

        elif choice == "3":
            view_logs()

        elif choice == "4":
            break

        else:
            print("Invalid Choice! Please try again.")
