# =============================================================================
# FILE NAME : retrieved.py
#
# PROJECT :
# Email Automation System
#
# MODULE :
# Data Retrieval System
#
# DESCRIPTION :
# This module retrieves stored data from different email automation modules.
#
# DATABASE :
# email_automation
#
# TABLES USED:
# email_reports
# contacts
# email_reminders
# email_drafts
# email_templates
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
# CLASS NAME : RetrieveData
#
# PURPOSE:
# Handles all data retrieval operations.
#
# =============================================================================


class RetrieveData:



    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================


    def __init__(self):


        self.conn = db_connection()



        if self.conn is None:


            print("Database connection failed.")






    # =========================================================================
    # FUNCTION NAME : search_email
    #
    # PURPOSE:
    # Search emails using receiver email or subject.
    #
    # TABLE:
    # email_reports
    #
    # =========================================================================


    def search_email(self):


        if self.conn is None:


            return




        print("\n================================")

        print("          SEARCH EMAIL")

        print("================================")


        print("1. Search By Receiver")

        print("2. Search By Subject")



        choice = input(

            "Enter Choice : "

        )



        cursor = self.conn.cursor()



        try:



            if choice == "1":



                receiver = input(

                    "Enter Receiver Email : "

                )



                query = """


                SELECT

                recipient_email,

                subject,

                sent_date,

                status


                FROM email_reports


                WHERE recipient_email LIKE %s


                """



                cursor.execute(

                    query,

                    (

                        "%" + receiver + "%",

                    )

                )




            elif choice == "2":



                subject = input(

                    "Enter Subject : "

                )




                query = """


                SELECT

                recipient_email,

                subject,

                sent_date,

                status


                FROM email_reports


                WHERE subject LIKE %s


                """



                cursor.execute(

                    query,

                    (

                        "%" + subject + "%",

                    )

                )




            else:



                print("\nInvalid Choice")

                return






            records = cursor.fetchall()




            self.display_email_records(records)





        except Error as err:


            print("\nSearch Error:")

            print(err)




        finally:



            cursor.close()







    # =========================================================================
    # FUNCTION NAME : filter_by_date
    #
    # PURPOSE:
    # Displays emails between selected dates.
    #
    # TABLE:
    # email_reports
    #
    # =========================================================================


    def filter_by_date(self):


        if self.conn is None:


            return




        start_date = input(

            "\nEnter Start Date (YYYY-MM-DD): "

        )



        end_date = input(

            "Enter End Date (YYYY-MM-DD): "

        )




        cursor = self.conn.cursor()



        try:



            query = """


            SELECT


            recipient_email,

            subject,

            sent_date,

            status



            FROM email_reports



            WHERE DATE(sent_date)

            BETWEEN %s AND %s



            ORDER BY sent_date



            """




            cursor.execute(

                query,

                (

                    start_date,

                    end_date

                )

            )




            records = cursor.fetchall()




            self.display_email_records(records)





        except Error as err:



            print("\nDate Filter Error:")

            print(err)




        finally:



            cursor.close()







    # =========================================================================
    # FUNCTION NAME : display_email_records
    #
    # PURPOSE:
    # Displays email records in formatted form.
    #
    # =========================================================================


    def display_email_records(self, records):


        if len(records) == 0:



            print("\nNo Email Records Found.")

            return





        print("\n================================================")

        print("                EMAIL RECORDS")

        print("================================================")



        print(

            "{:<30}{:<25}{:<25}{:<15}".format(

                "Receiver",

                "Subject",

                "Date",

                "Status"

            )

        )



        print("-"*100)




        for row in records:



            print(

                "{:<30}{:<25}{:<25}{:<15}".format(

                    str(row[0]),

                    str(row[1]),

                    str(row[2]),

                    str(row[3])

                )

            )

    # =========================================================================
    # FUNCTION NAME : view_status_records
    #
    # PURPOSE:
    # Displays emails based on status.
    #
    # STATUS:
    # Success / Failed
    #
    # TABLE:
    # email_reports
    #
    # =========================================================================


    def view_status_records(self):


        if self.conn is None:


            return




        print("\n================================")

        print("          EMAIL STATUS")

        print("================================")

        print("1. Successful Emails")

        print("2. Failed Emails")




        choice = input(

            "Enter Choice : "

        )




        if choice == "1":


            status = "Success"



        elif choice == "2":


            status = "Failed"



        else:


            print("\nInvalid Choice.")

            return





        cursor = self.conn.cursor()



        try:



            cursor.execute("""


            SELECT


            recipient_email,

            subject,

            sent_date,

            status



            FROM email_reports



            WHERE status=%s



            ORDER BY sent_date DESC



            """,

            (

                status,

            )

            )




            records = cursor.fetchall()




            self.display_email_records(records)




        except Error as err:



            print("\nStatus Fetch Error:")

            print(err)




        finally:



            cursor.close()







        # =========================================================================
    # FUNCTION NAME : view_drafts
    #
    # PURPOSE:
    # Displays saved email drafts.
    #
    # TABLE:
    # drafts
    #
    # =========================================================================

    def view_drafts(self):

        if self.conn is None:

            return

        cursor = self.conn.cursor()

        try:

            cursor.execute("""

                SELECT

                    id,

                    receiver_email,

                    subject,

                    created_on

                FROM drafts

                ORDER BY created_on DESC

            """)

            records = cursor.fetchall()

            print("\n================================")
            print("          DRAFT EMAILS")
            print("================================")

            if len(records) == 0:

                print("No Drafts Found.")

            else:

                print(
                    "{:<8}{:<35}{:<35}{:<25}".format(
                        "ID",
                        "Receiver",
                        "Subject",
                        "Created On"
                    )
                )

                print("-" * 105)

                for row in records:

                    print(
                        "{:<8}{:<35}{:<35}{:<25}".format(
                            row[0],
                            row[1],
                            row[2],
                            str(row[3])
                        )
                    )

        except Error as err:

            print("\nDraft Fetch Error :")
            print(err)

        finally:

            cursor.close()


    # =========================================================================
    # FUNCTION NAME : view_contacts
    #
    # PURPOSE:
    # Displays saved contacts.
    #
    # TABLE:
    # contacts
    #
    # =========================================================================


    def view_contacts(self):


        if self.conn is None:


            return




        cursor = self.conn.cursor()



        try:



            cursor.execute("""


            SELECT


            contact_id,

            name,

            email



            FROM contacts



            ORDER BY name



            """)




            records = cursor.fetchall()




            print("\n================================")

            print("             CONTACTS")

            print("================================")




            if len(records)==0:


                print("No Contacts Found.")



            else:



                print(

                    "{:<10}{:<25}{:<35}".format(

                        "ID",

                        "Name",

                        "Email"

                    )

                )



                print("-"*70)



                for row in records:



                    print(

                        "{:<10}{:<25}{:<35}".format(

                            row[0],

                            row[1],

                            row[2]

                        )

                    )




        except Error as err:



            print("\nContact Fetch Error:")

            print(err)




        finally:



            cursor.close()

    # =========================================================================
    # FUNCTION NAME : view_email_history
    #
    # PURPOSE:
    # Displays all sent email records.
    #
    # TABLE:
    # email_reports
    #
    # =========================================================================


    def view_email_history(self):


        if self.conn is None:

            return



        cursor = self.conn.cursor()



        try:


            cursor.execute("""


            SELECT


            recipient_email,

            subject,

            sent_date,

            status



            FROM email_reports



            ORDER BY sent_date DESC



            """)



            records = cursor.fetchall()



            print("\n==========================================")

            print("             EMAIL HISTORY")

            print("==========================================")



            if len(records)==0:


                print("No Email History Found.")



            else:



                print(

                    "{:<30}{:<25}{:<25}{:<15}".format(

                        "Recipient",

                        "Subject",

                        "Sent Date",

                        "Status"

                    )

                )



                print("-"*100)




                for row in records:



                    print(

                        "{:<30}{:<25}{:<25}{:<15}".format(

                            str(row[0]),

                            str(row[1]),

                            str(row[2]),

                            str(row[3])

                        )

                    )




        except Error as err:


            print("\nEmail History Error :",err)




        finally:


            cursor.close()






    # =========================================================================
    # FUNCTION NAME : view_scheduled_emails
    #
    # PURPOSE:
    # Displays scheduled email reminders.
    #
    # TABLE:
    # email_reminders
    #
    # =========================================================================


    def view_scheduled_emails(self):


        if self.conn is None:

            return



        cursor = self.conn.cursor()



        try:



            cursor.execute("""


            SELECT


            recipient_email,

            subject,

            reminder_date,

            status



            FROM email_reminders



            ORDER BY reminder_date



            """)




            records = cursor.fetchall()



            print("\n==========================================")

            print("          SCHEDULED EMAILS")

            print("==========================================")



            if len(records)==0:


                print("No Scheduled Emails Found.")



            else:



                print(

                    "{:<30}{:<25}{:<25}{:<15}".format(

                        "Recipient",

                        "Subject",

                        "Reminder Date",

                        "Status"

                    )

                )



                print("-"*100)




                for row in records:



                    print(

                        "{:<30}{:<25}{:<25}{:<15}".format(

                            str(row[0]),

                            str(row[1]),

                            str(row[2]),

                            str(row[3])

                        )

                    )




        except Error as err:



            print("\nScheduled Email Error :",err)




        finally:


            cursor.close()







    # =========================================================================
    # FUNCTION NAME : retrieve_menu
    #
    # PURPOSE:
    # Main menu of retrieval module.
    #
    # =========================================================================



    def retrieve_menu(self):



        while True:



            print("\n====================================")

            print("        DATA RETRIEVAL MODULE")

            print("====================================")

            print("1. View Contacts")

            print("2. View Email History")

            print("3. View Scheduled Emails")

            print("4. Search Emails")

            print("5. View Draft Emails")

            print("6. Filter Emails By Date")

            print("7. View Success / Failed Emails")

            print("8. Back")

            print("====================================")



            choice=input(

                "Enter Choice : "

            )



            if choice=="1":


                self.view_contacts()



            elif choice=="2":


                self.view_email_history()



            elif choice=="3":


                self.view_scheduled_emails()



            elif choice=="4":


                self.search_email()



            elif choice=="5":


                self.view_drafts()


            elif choice=="6":


                self.filter_by_date()



            elif choice=="7":


                self.view_status_records()



            elif choice=="8":


                print("\nReturning To Main Menu...")

                break



            else:


                print("\nInvalid Choice.")







    # =========================================================================
    # FUNCTION NAME : close_connection
    #
    # PURPOSE:
    # Closes MySQL connection.
    #
    # =========================================================================



    def close_connection(self):


        if self.conn:



            self.conn.close()

            print("\nDatabase Connection Closed.")





# =============================================================================
# MAIN PROGRAM
# =============================================================================


if __name__=="__main__":



    retrieve = RetrieveData()



    if retrieve.conn:



        retrieve.retrieve_menu()



        retrieve.close_connection()



    else:



        print("\nUnable To Connect Database.")