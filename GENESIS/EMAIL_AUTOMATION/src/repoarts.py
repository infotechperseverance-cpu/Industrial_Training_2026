# =============================================================================
# FILE NAME : reports.py
#
# PROJECT :
# Email Automation System
#
# MODULE :
# Email Report Management
#
# DESCRIPTION:
# Stores and displays email sending reports.
#
# DATABASE:
# email_automation
#
# TABLE:
# email_reports
#
# =============================================================================


import mysql.connector

from mysql.connector import Error




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



    except Error as err:


        print("\nDatabase Connection Error:")

        print(err)


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


    CREATE TABLE IF NOT EXISTS email_reports


    (

        id INT AUTO_INCREMENT PRIMARY KEY,


        recipient_email VARCHAR(255),


        subject VARCHAR(255),


        status VARCHAR(50),


        sent_date DATETIME DEFAULT CURRENT_TIMESTAMP


    )


    """



    cursor.execute(query)



    conn.commit()



    cursor.close()


    conn.close()






# =============================================================================
# ADD REPORT
#
# Used by:
# bulk_email.py
# approval.py
# follow_up.py
#
# =============================================================================


def add_report(recipient_email, subject, status):


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


        VALUES(%s,%s,%s)


        """,

        (

            recipient_email,

            subject,

            status

        )

        )



        conn.commit()



        print("Report Added Successfully.")



    except Error as err:


        print("\nReport Insert Error:")

        print(err)



    finally:


        cursor.close()

        conn.close()





# =============================================================================
# VIEW REPORTS
# =============================================================================


def show_report():


    conn = db_connection()



    if conn is None:


        return



    cursor = conn.cursor()



    cursor.execute("""


    SELECT *

    FROM email_reports

    ORDER BY sent_date DESC


    """)



    records = cursor.fetchall()



    print("\n================================")

    print("          EMAIL REPORTS")

    print("================================")



    if len(records)==0:


        print("No Reports Found.")



    else:



        for row in records:


            print("--------------------------------")

            print("ID              :",row[0])

            print("Receiver Email  :",row[1])

            print("Subject         :",row[2])

            print("Status          :",row[3])

            print("Date            :",row[4])



    cursor.close()

    conn.close()






# =============================================================================
# REPORT STATISTICS
# =============================================================================


def statistics():


    conn = db_connection()



    if conn is None:


        return



    cursor = conn.cursor()



    cursor.execute(

        "SELECT COUNT(*) FROM email_reports"

    )


    total = cursor.fetchone()[0]




    cursor.execute("""


    SELECT COUNT(*)

    FROM email_reports

    WHERE status='Success'


    """)



    success = cursor.fetchone()[0]





    cursor.execute("""


    SELECT COUNT(*)

    FROM email_reports

    WHERE status='Failed'


    """)



    failed = cursor.fetchone()[0]





    if total == 0:


        rate = 0



    else:


        rate = (success / total) * 100





    print("\n================================")

    print("        REPORT STATISTICS")

    print("================================")



    print("Total Emails :", total)

    print("Successful   :", success)

    print("Failed       :", failed)

    print(

        "Success Rate : {:.2f}%".format(rate)

    )




    cursor.close()

    conn.close()





# =============================================================================
# REPORT MENU
# =============================================================================


def report_menu():


    create_table()



    while True:



        print("\n================================")

        print("          EMAIL REPORT MENU")

        print("================================")


        print("1. Add Report")

        print("2. View Reports")

        print("3. Statistics")

        print("4. Exit")


        print("================================")



        choice=input(

            "Enter Choice : "

        )




        if choice=="1":



            email=input(

                "Receiver Email : "

            )


            subject=input(

                "Subject : "

            )


            status=input(

                "Status (Success/Failed): "

            )



            add_report(

                email,

                subject,

                status

            )



        elif choice=="2":


            show_report()



        elif choice=="3":


            statistics()



        elif choice=="4":


            print("\nThank You.")

            break



        else:


            print("\nInvalid Choice.")





# =============================================================================
# MAIN PROGRAM
# =============================================================================


if __name__=="__main__":


    report_menu()