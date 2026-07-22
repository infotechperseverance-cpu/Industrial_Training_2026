import mysql.connector

# ---------------- DATABASE CONNECTION ----------------
def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pass@123",      # MySQL password
        database="bulk_email_system"
    )

# ---------------- CREATE TABLE ----------------
def create_table():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_reports (
        id INT AUTO_INCREMENT PRIMARY KEY,
        recipient_email VARCHAR(100),
        subject VARCHAR(255),
        status VARCHAR(20),
        sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()



# ---------------- INSERT REPORT ----------------
def add_report(recipient_email, subject, status):
    conn = db_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO email_reports(recipient_email, subject, status)
    VALUES (%s,%s,%s)
    """

    cursor.execute(sql, (recipient_email, subject, status))
    conn.commit()
    conn.close()

# ---------------- SHOW REPORT ----------------
def show_report():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM email_reports")

    data = cursor.fetchall()

    print("\n========= EMAIL REPORT =========")
    for row in data:
        print(row)

    conn.close()

# ---------------- STATISTICS ----------------
def statistics():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM email_reports")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM email_reports WHERE status='Success'")
    success = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM email_reports WHERE status='Failed'")
    failed = cursor.fetchone()[0]

    if total == 0:
        rate = 0
    else:
        rate = (success / total) * 100

    print("\n========= REPORT STATISTICS =========")
    print("Total Emails :", total)
    print("Successful   :", success)
    print("Failed       :", failed)
    print("Success Rate : {:.2f}%".format(rate))

    conn.close()

# ---------------- MAIN ----------------

create_table()

while True:
    print("\n===== REPORT MENU =====")
    print("1. Add Report")
    print("2. View Reports")
    print("3. Statistics")
    print("4. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        email = input("Recipient Email : ")
        subject = input("Subject : ")
        status = input("Status (Success/Failed): ")

        add_report(email, subject, status)
        print("Report Saved Successfully.")

    elif choice == "2":
        show_report()

    elif choice == "3":
        statistics()

    elif choice == "4":
        print("Thank You")
        break

    else:
        print("Invalid Choice")