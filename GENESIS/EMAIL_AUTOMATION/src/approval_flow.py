import smtplib
import ssl
import mysql.connector

# -----------------------------------------------------------------------------
# DATABASE CONNECTION
# -----------------------------------------------------------------------------
def db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pass@123",  # Replace MySQL password here
            database="email_login"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"\n[Database Error]: {err}")
        return None

# -----------------------------------------------------------------------------
# TABLE SETUP
# -----------------------------------------------------------------------------
def setup_approval_table():
    """
    Creates the 'email_approvals' table if it does not already exist.
    """
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS email_approvals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_email VARCHAR(255),
            receiver_email VARCHAR(255),
            subject VARCHAR(255),
            body TEXT,
            status VARCHAR(50) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

# -----------------------------------------------------------------------------
# USER FUNCTIONALITY (Submit Request)
# -----------------------------------------------------------------------------
def request_email_approval(sender_email):
    """
    Allows a junior user/employee to draft an email and submit it for manager approval.
    """
    setup_approval_table()
    print("\n--- SUBMIT EMAIL FOR APPROVAL (User Mode) ---")
    receiver_email = input("Recipient Email: ").strip()
    subject = input("Subject: ").strip()
    body = input("Message Body: ").strip()

    if not receiver_email or not subject or not body:
        print("\n[Error] All fields are required!")
        return

    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        INSERT INTO email_approvals (sender_email, receiver_email, subject, body, status)
        VALUES (%s, %s, %s, %s, 'Pending')
        """
        cursor.execute(query, (sender_email, receiver_email, subject, body))
        conn.commit()
        print("\n[Success] Email submitted for approval! Status set to 'Pending'.")
        cursor.close()
        conn.close()

# -----------------------------------------------------------------------------
# MANAGER FUNCTIONALITY (Review & Approve/Reject)
# -----------------------------------------------------------------------------
def review_and_approve_emails(manager_email, manager_password):
    """
    Allows a manager/admin to view pending email requests and Approve or Reject them.
    If Approved, the email is sent immediately using SMTP.
    """
    setup_approval_table()
    print("\n--- MANAGER APPROVAL PANEL (Manager Mode) ---")
    
    conn = db_connection()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT id, sender_email, receiver_email, subject, body FROM email_approvals WHERE status = 'Pending'")
    pending_emails = cursor.fetchall()

    if not pending_emails:
        print("\n[Info] No pending email requests found.")
        cursor.close()
        conn.close()
        return

    print("\n--- PENDING EMAIL REQUESTS ---")
    print(f"{'ID':<5} | {'From':<25} | {'To':<25} | {'Subject':<20}")
    print("-" * 80)
    for item in pending_emails:
        print(f"{item[0]:<5} | {item[1]:<25} | {item[2]:<25} | {item[3]:<20}")

    request_id = input("\nEnter Email ID to action (or press Enter to go back): ").strip()
    if not request_id:
        cursor.close()
        conn.close()
        return

    cursor.execute("SELECT sender_email, receiver_email, subject, body FROM email_approvals WHERE id = %s AND status = 'Pending'", (request_id,))
    selected_email = cursor.fetchone()

    if not selected_email:
        print("\n[Error] Invalid Email ID selected.")
        cursor.close()
        conn.close()
        return

    action = input("Type 'A' to Approve & Send OR 'R' to Reject (A/R): ").strip().upper()

    if action == 'A':
        try:
            smtp_host = "smtp.gmail.com"
            smtp_port = 465
            my_context = ssl.create_default_context()
            msg = f"Subject: {selected_email[2]}\n\n{selected_email[3]}"

            server = smtplib.SMTP_SSL(smtp_host, smtp_port, context=my_context)
            server.login(manager_email, manager_password)
            server.sendmail(manager_email, selected_email[1], msg)
            server.quit()

            cursor.execute("UPDATE email_approvals SET status = 'Approved' WHERE id = %s", (request_id,))
            conn.commit()
            print(f"\n[Success] Email approved and successfully sent to {selected_email[1]}!")
        except Exception as e:
            print(f"\n[Error] Failed to send email: {e}")
    elif action == 'R':
        cursor.execute("UPDATE email_approvals SET status = 'Rejected' WHERE id = %s", (request_id,))
        conn.commit()
        print("\n[Info] Email request has been Rejected.")
    else:
        print("\n[Error] Invalid action selected.")

    cursor.close()
    conn.close()

# -----------------------------------------------------------------------------
# MAIN MODULE WORKFLOW MENU
# -----------------------------------------------------------------------------
def approval_workflow_menu(authenticated_user=None, saved_password=None):
    """
    Main menu driver for Email Approval Workflow. Called directly from main.py.
    """
    if not authenticated_user:
        authenticated_user = input("Enter your Email ID: ").strip()
        saved_password = input("Enter your App Password: ").strip()

    while True:
        print("\n=========================================")
        print("     EMAIL APPROVAL WORKFLOW MODULE      ")
        print("=========================================")
        print("1. User Mode: Submit Email for Approval")
        print("2. Manager Mode: Review & Approve Emails")
        print("3. Back to Main System Menu")
        print("=========================================")
        
        choice = input("Select Option (1-3): ").strip()
        
        if choice == '1':
            request_email_approval(authenticated_user)
        elif choice == '2':
            review_and_approve_emails(authenticated_user, saved_password)
        elif choice == '3':
            print("Returning to Main Menu...")
            break
        else:
            print("\n[Error] Invalid choice! Please select 1, 2, or 3.")
