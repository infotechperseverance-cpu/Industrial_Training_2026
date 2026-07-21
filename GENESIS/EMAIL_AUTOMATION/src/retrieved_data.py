import mysql.connector

# -----------------------------
# Database Connection
# -----------------------------
def db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="system@123",
            database="email_login"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"\nDatabase Error : {err}")
        return None


# -----------------------------
# Retrieve Data Class
# -----------------------------
class RetrieveData:

    def __init__(self):
        self.conn = db_connection()


# FUNCTION NAME: search_email
# WHAT IT DOES: Allows the user to search sent emails either by
#               recipient email address or by email subject.
#               It retrieves matching records from the email_history
#               table and displays them in a formatted manner.
# INPUTS: None (takes user input for search criteria)
# OUTPUT: Displays matching email records on the screen.
    def search_email(self):

         # Displaying search options to the user
        print("\nSearch By")
        print("1. Recipient")
        print("2. Subject")

        choice = input("Enter Choice : ")

        # Creating database cursor
        cursor = self.conn.cursor()

        # Searching emails using recipient email
        if choice == "1":

            # Taking recipient email from user
            recipient = input("Enter Recipient Email : ")

             # SQL query to search matching recipient emails
            query = """
            SELECT recipient, subject, sent_date, status
            FROM email_history
            WHERE recipient LIKE %s
            """

             # Executing query
            cursor.execute(query, ("%" + recipient + "%",))

         # SQL query to search matching subjects
        elif choice == "2":

            subject = input("Enter Subject : ")

            query = """
            SELECT recipient, subject, sent_date, status
            FROM email_history
            WHERE subject LIKE %s
            """

            cursor.execute(query, ("%" + subject + "%",))

        else:
            print("Invalid Choice")
            cursor.close()
            return

        # Fetching all matching records
        records = cursor.fetchall()

         # Checking whether any records are found
        if len(records) == 0:
            print("\nNo Records Found")

        else:

            print("\nSearch Result\n")

            # Displaying search results
            print("{:<30}{:<25}{:<25}{:<15}".format(
                "Recipient",
                "Subject",
                "Date",
                "Status"
            ))

            print("-"*95)

            for row in records:

                print("{:<30}{:<25}{:<25}{:<15}".format(
                    str(row[0]),
                    str(row[1]),
                    str(row[2]),
                    str(row[3])
                ))

        cursor.close()

# FUNCTION NAME: filter_by_date
# WHAT IT DOES: Filters and displays email records from the
#               email_history table between the start date
#               and end date entered by the user.
# INPUTS: None (takes start date and end date from the user)
# OUTPUT: Displays all email records found within the given date range.

    def filter_by_date(self):
             # Taking start date and end date from the user
            start_date = input("\nEnter Start Date (YYYY-MM-DD): ").strip()
            end_date = input("Enter End Date (YYYY-MM-DD): ").strip()

            cursor = self.conn.cursor()

            query = """
            SELECT recipient, subject, sent_date, status
            FROM email_history
            WHERE DATE(sent_date) BETWEEN %s AND %s
            ORDER BY sent_date
            """

            try:

                cursor.execute(query, (start_date, end_date))

                records = cursor.fetchall()

                if len(records) == 0:

                    print("\nNo Emails Found Between These Dates.")

                else:

                    print("\n============= FILTERED EMAILS =============")

                    print("{:<30}{:<25}{:<25}{:<15}".format(
                        "Recipient",
                        "Subject",
                        "Sent Date",
                        "Status"
                    ))

                    print("-" * 100)

                    # Displaying each matching email record
                    for row in records:

                        print("{:<30}{:<25}{:<25}{:<15}".format(
                            str(row[0]),
                            str(row[1]),
                            str(row[2]),
                            str(row[3])
                        ))
            
            # Handling database-related errors
            except mysql.connector.Error as err:
                print("\nDatabase Error:", err)

            cursor.close()

# FUNCTION NAME: view_status_records
# WHAT IT DOES: Displays email records based on their sending status.
#               The user can choose to view either successful or
#               failed emails from the email_history table.
# INPUTS: None (takes user choice for email status)
# OUTPUT: Displays email records with the selected status.

    def view_status_records(self):

        print("\n========== EMAIL STATUS ==========")
        print("1. Successful Emails")
        print("2. Failed Emails")

        choice = input("Enter Choice : ").strip()

        if choice == "1":
            status = "Success"

        elif choice == "2":
            status = "Failed"

        else:
            print("\nInvalid Choice")
            return

        cursor = self.conn.cursor()

        query = """
        SELECT recipient, subject, sent_date, status
        FROM email_history
        WHERE status = %s
        ORDER BY sent_date DESC
        """

        try:

            cursor.execute(query, (status,))

            records = cursor.fetchall()

            if len(records) == 0:

                print(f"\nNo {status} Email Records Found.")

            else:

                print(f"\n========== {status.upper()} EMAILS ==========")

                print("{:<30}{:<25}{:<25}{:<15}".format(
                    "Recipient",
                    "Subject",
                    "Sent Date",
                    "Status"
                ))

                print("-" * 100)

                for row in records:

                    print("{:<30}{:<25}{:<25}{:<15}".format(
                        str(row[0]),
                        str(row[1]),
                        str(row[2]),
                        str(row[3])
                    ))

        except mysql.connector.Error as err:
            print("\nDatabase Error:", err)

        cursor.close()

# FUNCTION NAME: view_drafts
# WHAT IT DOES: Retrieves and displays all saved draft emails
#               from the drafts table in descending order of
#               their creation date.
# INPUTS: None
# OUTPUT: Displays the recipient, subject, and created date
#         of all draft emails.
    def view_drafts(self):

        cursor = self.conn.cursor()

        query = """
        SELECT recipient, subject, created_date
        FROM drafts
        ORDER BY created_date DESC
        """

        try:

            cursor.execute(query)

            records = cursor.fetchall()

            if len(records) == 0:

                print("\nNo Draft Emails Found.")

            else:

                print("\n=============== DRAFT EMAILS ===============")

                print("{:<30}{:<30}{:<25}".format(
                    "Recipient",
                    "Subject",
                    "Created Date"
                ))

                print("-" * 90)

                for row in records:

                    print("{:<30}{:<30}{:<25}".format(
                        str(row[0]),
                        str(row[1]),
                        str(row[2])
                    ))

        except mysql.connector.Error as err:
            print("\nDatabase Error:", err)

        cursor.close()

# FUNCTION NAME: view_templates
# WHAT IT DOES: Retrieves all available email templates from the
#               templates table and displays them. It also allows
#               the user to select a template by its ID and view
#               the complete subject and body of that template.
# INPUTS: None (takes template ID from the user)
# OUTPUT: Displays the list of templates and the selected
#         template details.
    def view_templates(self):

        cursor = self.conn.cursor()

        query = """
        SELECT template_id,
            template_name,
            subject
        FROM templates
        ORDER BY template_name
        """

        try:

            cursor.execute(query)

            # Fetching all template records
            records = cursor.fetchall()

             # Checking whether any templates exist
            if len(records) == 0:

                print("\nNo Email Templates Found.")

            else:
                 # Displaying all available email templates
                print("\n=============== EMAIL TEMPLATES ===============")

                print("{:<10}{:<30}{:<35}".format(
                    "ID",
                    "Template Name",
                    "Subject"
                ))

                print("-" * 80)

                for row in records:

                    print("{:<10}{:<30}{:<35}".format(
                        row[0],
                        row[1],
                        row[2]
                    ))

                # Taking template ID from the user
                template_id = input("\nEnter Template ID to View (0 to Back): ").strip()
                # Returning to the previous menu if user enters 0
                if template_id == "0":
                    cursor.close()
                    return

                # SQL query to retrieve complete details of the selected template
                query = """
                SELECT template_name,
                    subject,
                    body
                FROM templates
                WHERE template_id = %s
                """

                cursor.execute(query, (template_id,))

                record = cursor.fetchone()
                 
                 # Checking whether the template exists
                if record:

                    print("\n========== TEMPLATE DETAILS ==========")
                    print("Template Name :", record[0])
                    print("Subject       :", record[1])
                    print("\nBody:\n")
                    print(record[2])

                else:
                    print("\nInvalid Template ID.")

        except mysql.connector.Error as err:
            print("\nDatabase Error:", err)

        cursor.close()

    # -----------------------------
    # Main Menu
    # -----------------------------
    def retrieve_menu(self):

        while True:

            print("\n==========================================")
            print("         DATA RETRIEVAL MODULE")
            print("==========================================")
            print("1. Retrieve Saved Contacts")
            print("2. View Sent Email History")
            print("3. View Scheduled Emails")
            print("4. Search Emails")
            print("5. View Draft Emails")
            print("6. Retrieve Email Templates")
            print("7. Filter Emails by Date")
            print("8. Show Successful / Failed Emails")
            print("9. Back")
            print("==========================================")

            choice = input("Enter Choice : ")

            if choice == "1":
                self.view_contacts()

            elif choice == "2":
                self.view_email_history()

            elif choice == "3":
                self.view_scheduled_emails()

            elif choice == "4":
                self.search_email()

            elif choice == "5":
                self.view_drafts()

            elif choice == "6":
                self.view_templates()

            elif choice == "7":
                self.filter_by_date()

            elif choice == "8":
                self.view_status_records()

            elif choice == "9":
                print("\nReturning to Main Menu...")
                return

            else:
                print("\nInvalid Choice")


    # -----------------------------
    # View Contacts
    # -----------------------------
    def view_contacts(self):

        cursor = self.conn.cursor()

        query = "SELECT * FROM contacts"

        cursor.execute(query)

        records = cursor.fetchall()

        print("\n=============== CONTACTS ===============")

        if len(records) == 0:
            print("No Contacts Found")

        else:

            print("{:<10}{:<25}{:<30}".format(
                "ID",
                "NAME",
                "EMAIL"
            ))

            print("-"*65)

            for row in records:

                print("{:<10}{:<25}{:<30}".format(
                    row[0],
                    row[1],
                    row[2]
                ))

        cursor.close()


    # -----------------------------
    # View Email History
    # -----------------------------
    def view_email_history(self):

        cursor = self.conn.cursor()

        query = """
        SELECT
        recipient,
        subject,
        sent_date,
        status
        FROM email_history
        """

        cursor.execute(query)

        records = cursor.fetchall()

        print("\n================ EMAIL HISTORY ================")

        if len(records) == 0:

            print("No Email History Found")

        else:

            print("{:<30}{:<25}{:<25}{:<15}".format(
                "Recipient",
                "Subject",
                "Sent Date",
                "Status"
            ))

            print("-"*95)

            for row in records:

                print("{:<30}{:<25}{:<25}{:<15}".format(
                    str(row[0]),
                    str(row[1]),
                    str(row[2]),
                    str(row[3])
                ))

        cursor.close()


    # -----------------------------
    # View Scheduled Emails
    # -----------------------------
    def view_scheduled_emails(self):

        cursor = self.conn.cursor()

        query = """
        SELECT
        recipient,
        subject,
        schedule_time,
        status
        FROM scheduled_emails
        """

        cursor.execute(query)

        records = cursor.fetchall()

        print("\n=============== SCHEDULED EMAILS ===============")

        if len(records) == 0:

            print("No Scheduled Emails")

        else:

            print("{:<30}{:<25}{:<25}{:<15}".format(
                "Recipient",
                "Subject",
                "Schedule Time",
                "Status"
            ))

            print("-"*100)

            for row in records:

                print("{:<30}{:<25}{:<25}{:<15}".format(
                    str(row[0]),
                    str(row[1]),
                    str(row[2]),
                    str(row[3])
                ))

        cursor.close()


