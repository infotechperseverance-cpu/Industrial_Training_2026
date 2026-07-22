# =============================================================================
# FILE NAME : follow_up.py
#
# PROJECT : Email Automation System
#
# MODULE :
# Follow-Up Email Management System
#
# DESCRIPTION :
# This module sends follow-up emails to saved contacts.
#
# FEATURES :
# 1. Select contact from database
# 2. Send follow-up Gmail
# 3. Store follow-up history
# 4. Store email reports for dashboard
#
# DATABASE :
# email_automation
#
# TABLES USED :
# contacts
# follow_up_history
# email_reports
#
# =============================================================================


import smtplib
import ssl
import re

import mysql.connector


from mysql.connector import Error


from email.message import EmailMessage


from datetime import datetime





# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================


HOST = "localhost"

USER = "root"

PASSWORD = "root123"

DATABASE = "email_automation"





# =============================================================================
# FUNCTION NAME : db_connection
#
# PURPOSE :
# Creates MySQL database connection.
#
# RETURNS :
# Connection Object / None
#
# =============================================================================


def db_connection():


    try:


        connection = mysql.connector.connect(


            host=HOST,

            user=USER,

            password=PASSWORD,

            database=DATABASE


        )


        return connection




    except Error as err:


        print("\n===================================")

        print("DATABASE CONNECTION ERROR")

        print("===================================")

        print(err)


        return None







# =============================================================================
# FUNCTION NAME : check_email
#
# PURPOSE :
# Validates Gmail Address.
#
# RETURNS :
# True / False
#
# =============================================================================


def check_email(email):


    pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'


    return bool(

        re.fullmatch(

            pattern,

            email

        )

    )









# =============================================================================
# FUNCTION NAME : create_tables
#
# PURPOSE :
# Creates required tables.
#
# TABLES :
# 1. follow_up_history
# 2. email_reports
#
# =============================================================================



def create_tables():


    conn = db_connection()



    if conn is None:


        return



    cursor = None



    try:


        cursor = conn.cursor()




        # -------------------------------------------------------------
        # FOLLOW UP HISTORY TABLE
        # -------------------------------------------------------------



        cursor.execute("""


        CREATE TABLE IF NOT EXISTS follow_up_history

        (

            id INT AUTO_INCREMENT PRIMARY KEY,


            receiver_email VARCHAR(255),


            subject VARCHAR(255),


            message TEXT,


            sent_time DATETIME DEFAULT CURRENT_TIMESTAMP,


            status VARCHAR(50)


        )


        """)






        # -------------------------------------------------------------
        # EMAIL REPORT TABLE
        # Dashboard Integration
        # -------------------------------------------------------------



        cursor.execute("""


        CREATE TABLE IF NOT EXISTS email_reports

        (

            id INT AUTO_INCREMENT PRIMARY KEY,


            recipient_email VARCHAR(255),


            subject VARCHAR(255),


            status VARCHAR(50),


            sent_date DATETIME DEFAULT CURRENT_TIMESTAMP


        )


        """)





        conn.commit()



        print("\nFollow-Up Tables Ready.")




    except Error as err:


        print("\nTable Creation Error")

        print(err)




    finally:


        if cursor:


            cursor.close()



        conn.close()







# =============================================================================
# CLASS NAME : FollowUpEmail
#
# PURPOSE :
# Handles all follow-up email operations.
#
# =============================================================================



class FollowUpEmail:




    # =========================================================================
    # CONSTRUCTOR
    #
    # INPUT :
    # sender_email
    # sender_password
    #
    # =========================================================================



    def __init__(self, sender_email, sender_password):



        create_tables()



        self.connection = db_connection()



        if self.connection is None:



            raise Exception(

                "Database Connection Failed"

            )




        self.cursor = self.connection.cursor(buffered=True)




        self.email = sender_email


        self.password = sender_password

# =============================================================================
# FUNCTION NAME : display_contacts
#
# PURPOSE :
# Displays all contacts stored in contacts table.
#
# =============================================================================


    def display_contacts(self):


        try:


            query = """

            SELECT

                contact_id,

                name,

                email


            FROM contacts


            ORDER BY name


            """



            self.cursor.execute(query)



            contacts = self.cursor.fetchall()




            print("\n====================================")

            print("             CONTACT LIST")

            print("====================================")




            if len(contacts) == 0:


                print("No Contacts Found.")

                return




            for row in contacts:


                print("------------------------------------")

                print("Contact ID :", row[0])

                print("Name       :", row[1])

                print("Email      :", row[2])



            print("------------------------------------")




        except Error as err:


            print("\nContact Fetch Error")

            print(err)







# =============================================================================
# FUNCTION NAME : get_contact_email
#
# PURPOSE :
# Returns email address using contact ID.
#
# INPUT :
# contact_id
#
# RETURN :
# Email Address
#
# =============================================================================



    def get_contact_email(self, contact_id):


        try:


            query = """

            SELECT email

            FROM contacts

            WHERE contact_id=%s


            """



            self.cursor.execute(

                query,

                (contact_id,)

            )



            result = self.cursor.fetchone()




            if result:


                return result[0]



            return None




        except Error as err:


            print("\nContact Search Error")

            print(err)


            return None







# =============================================================================
# FUNCTION NAME : save_followup
#
# PURPOSE :
# Saves follow-up email history.
#
# =============================================================================



    def save_followup(

            self,

            receiver,

            subject,

            message,

            status

    ):



        try:



            query = """

            INSERT INTO follow_up_history

            (

                receiver_email,

                subject,

                message,

                sent_time,

                status


            )


            VALUES

            (

                %s,

                %s,

                %s,

                %s,

                %s

            )


            """




            self.cursor.execute(

                query,

                (

                    receiver,

                    subject,

                    message,

                    datetime.now(),

                    status

                )

            )



            self.connection.commit()




        except Error as err:



            print("\nFollow-Up History Saving Error")

            print(err)







# =============================================================================
# FUNCTION NAME : save_report
#
# PURPOSE :
# Saves email sending report for dashboard.
#
# TABLE :
# email_reports
#
# =============================================================================



    def save_report(

            self,

            receiver,

            subject,

            status

    ):



        try:



            query = """

            INSERT INTO email_reports

            (

                recipient_email,

                subject,

                status


            )


            VALUES

            (

                %s,

                %s,

                %s

            )


            """




            self.cursor.execute(

                query,

                (

                    receiver,

                    subject,

                    status

                )

            )




            self.connection.commit()




        except Error as err:



            print("\nReport Saving Error")

            print(err)






# =============================================================================
# FUNCTION NAME : close_connection
#
# PURPOSE :
# Closes database connection.
#
# =============================================================================



    def close_connection(self):


        try:



            if self.cursor:


                self.cursor.close()




            if self.connection:


                self.connection.close()



        except Error as err:


            print("\nClosing Connection Error")

            print(err)

# =============================================================================
# FUNCTION NAME : send_followup
#
# PURPOSE :
# Sends follow-up email using Gmail SMTP.
#
# INPUT :
# receiver_email
# subject
# message
#
# OUTPUT :
# Sends email and stores history/report.
#
# =============================================================================


    def send_followup(

            self,

            receiver_email,

            subject,

            message

    ):



        if not check_email(receiver_email):


            print("\nInvalid Gmail Address.")

            return





        try:



            email = EmailMessage()



            email["From"] = self.email


            email["To"] = receiver_email


            email["Subject"] = "Follow-up : " + subject



            email.set_content(message)






            context = ssl.create_default_context()



            server = smtplib.SMTP_SSL(

                "smtp.gmail.com",

                465,

                context=context

            )



            server.login(

                self.email,

                self.password

            )



            server.send_message(email)



            server.quit()





            print("\n====================================")

            print("FOLLOW-UP EMAIL SENT SUCCESSFULLY")

            print("====================================")

            print("Receiver :", receiver_email)

            print("Time     :", datetime.now())






            self.save_followup(

                receiver_email,

                subject,

                message,

                "Success"

            )




            self.save_report(

                receiver_email,

                subject,

                "Success"

            )







        except Exception as err:



            print("\nEmail Sending Failed")

            print(err)



            self.save_followup(

                receiver_email,

                subject,

                message,

                "Failed"

            )



            self.save_report(

                receiver_email,

                subject,

                "Failed"

            )









# =============================================================================
# FUNCTION NAME : followup_menu
#
# PURPOSE :
# Main menu of follow-up module.
#
# =============================================================================



def followup_menu(sender_email, sender_password):



    followup = FollowUpEmail(

        sender_email,

        sender_password

    )



    while True:



        print("\n===================================")

        print("       FOLLOW-UP EMAIL SYSTEM")

        print("===================================")

        print("1. Send Follow-Up Email")

        print("2. View Contacts")

        print("3. Exit")

        print("===================================")




        choice = input(

            "Enter Choice : "

        ).strip()





        if choice == "1":



            followup.display_contacts()



            try:



                contact_id = int(

                    input(

                        "\nEnter Contact ID : "

                    )

                )



            except ValueError:



                print("\nInvalid Contact ID.")

                continue






            receiver = followup.get_contact_email(

                contact_id

            )





            if receiver is None:



                print("\nContact Not Found.")

                continue






            subject = input(

                "\nEnter Subject : "

            ).strip()





            if subject == "":



                print("Subject cannot be empty.")

                continue






            message = input(

                "Enter Follow-Up Message : "

            ).strip()





            if message == "":



                print("Message cannot be empty.")

                continue





            followup.send_followup(

                receiver,

                subject,

                message

            )








        elif choice == "2":



            followup.display_contacts()






        elif choice == "3":



            print("\nReturning To Main Menu...")

            break






        else:



            print("\nInvalid Choice.")





    followup.close_connection()







# =============================================================================
# MAIN PROGRAM
#
# NOTE:
# Normally main.py will call this module after login.
#
# =============================================================================



if __name__ == "__main__":



    print("\n===================================")

    print("       FOLLOW-UP EMAIL LOGIN")

    print("===================================")



    sender_email = input(

        "Enter Gmail ID : "

    ).strip()




    sender_password = input(

        "Enter Gmail App Password : "

    ).strip()





    if sender_email == "" or sender_password == "":


        print("\nLogin Required.")

        exit()





    followup_menu(

        sender_email,

        sender_password

    )