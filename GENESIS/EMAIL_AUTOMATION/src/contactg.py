# =============================================================================
# FILE NAME : contactg.py
#
# PROJECT : Email Automation System
#
# MODULE :
# Contact Group Management
#
# DESCRIPTION :
# This module manages Contact Groups and Contacts.
#
# FEATURES :
# 1. Create Group
# 2. View Groups
# 3. Add Contact
# 4. View Contacts
# 5. Update Contact
# 6. Delete Contact
# 7. Delete Group
#
# DATABASE :
# email_automation
#
# TABLES :
# contact_groups
# contacts
#
# =============================================================================

import re
import mysql.connector

from mysql.connector import Error

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

HOST = "localhost"
USER = "root"
PASSWORD = "root123"          # Change if required
DATABASE = "email_automation"

# =============================================================================
# FUNCTION NAME : db_connection
#
# PURPOSE :
# Connects to MySQL database.
#
# RETURNS :
# MySQL Connection Object
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
# =============================================================================

def check_email(email):

    pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'

    return bool(re.fullmatch(pattern, email))


# =============================================================================
# FUNCTION NAME : create_tables
#
# PURPOSE :
# Creates contact_groups and contacts tables.
#
# =============================================================================

def create_tables():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        # ----------------------------------------------------------
        # Contact Groups Table
        # ----------------------------------------------------------

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS contact_groups
        (

            group_id INT AUTO_INCREMENT PRIMARY KEY,

            group_name VARCHAR(100)

            UNIQUE NOT NULL

        )

        """)

        # ----------------------------------------------------------
        # Contacts Table
        # ----------------------------------------------------------

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS contacts
        (

            contact_id INT AUTO_INCREMENT PRIMARY KEY,

            name VARCHAR(100) NOT NULL,

            email VARCHAR(150)

            UNIQUE NOT NULL,

            group_id INT,

            FOREIGN KEY(group_id)

            REFERENCES contact_groups(group_id)

            ON DELETE CASCADE

        )

        """)

        conn.commit()

    except Error as err:

        print("\nTable Creation Error")
        print(err)

    finally:

        if cursor:

            cursor.close()

        conn.close()

# =============================================================================
# FUNCTION NAME : create_group
#
# PURPOSE :
# Creates a new contact group.
#
# =============================================================================

def create_group():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        print("\n===================================")
        print("        CREATE NEW GROUP")
        print("===================================")

        while True:

            group_name = input("Enter Group Name : ").strip()

            if group_name == "":

                print("Group Name cannot be empty.")
                continue

            break

        cursor.execute(

            "SELECT * FROM contact_groups WHERE group_name=%s",

            (group_name,)

        )

        if cursor.fetchone():

            print("\nGroup already exists.")

            return

        cursor.execute(

            "INSERT INTO contact_groups(group_name) VALUES(%s)",

            (group_name,)

        )

        conn.commit()

        print("\nGroup Created Successfully.")

    except Error as err:

        print("\nUnable to Create Group.")
        print(err)

    finally:

        if cursor:

            cursor.close()

        conn.close()


# =============================================================================
# FUNCTION NAME : view_groups
#
# PURPOSE :
# Displays all available groups.
#
# =============================================================================

def view_groups():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        cursor.execute(

            """

            SELECT

                group_id,

                group_name

            FROM contact_groups

            ORDER BY group_name

            """

        )

        groups = cursor.fetchall()

        print("\n===================================")
        print("          CONTACT GROUPS")
        print("===================================")

        if len(groups) == 0:

            print("No Groups Found.")

            return

        for row in groups:

            print("-----------------------------------")
            print("Group ID   :", row[0])
            print("Group Name :", row[1])

        print("-----------------------------------")

    except Error as err:

        print("\nUnable to Fetch Groups.")
        print(err)

    finally:

        if cursor:

            cursor.close()

        conn.close()


# =============================================================================
# FUNCTION NAME : add_contact
#
# PURPOSE :
# Adds a contact into a selected group.
#
# =============================================================================

def add_contact():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        print("\n===================================")
        print("          ADD NEW CONTACT")
        print("===================================")

        while True:

            name = input("Contact Name : ").strip()

            if name == "":

                print("Name cannot be empty.")
                continue

            break

        while True:

            email = input("Gmail Address : ").strip()

            if not check_email(email):

                print("Invalid Gmail Address.")
                continue

            break

        cursor.execute(

            "SELECT contact_id FROM contacts WHERE email=%s",

            (email,)

        )

        if cursor.fetchone():

            print("\nThis Email Already Exists.")

            return

        print("\nAvailable Groups")
        print("----------------")

        cursor.execute(

            "SELECT group_id, group_name FROM contact_groups"

        )

        groups = cursor.fetchall()

        if len(groups) == 0:

            print("No Groups Available.")
            print("Create a Group First.")

            return

        for group in groups:

            print(group[0], "-", group[1])

        group_id = input("\nEnter Group ID : ").strip()

        if not group_id.isdigit():

            print("Invalid Group ID.")

            return

        cursor.execute(

            "SELECT group_id FROM contact_groups WHERE group_id=%s",

            (group_id,)

        )

        if cursor.fetchone() is None:

            print("Group Not Found.")

            return

        cursor.execute(

            """

            INSERT INTO contacts

            (

                name,

                email,

                group_id

            )

            VALUES

            (

                %s,

                %s,

                %s

            )

            """,

            (

                name,

                email,

                group_id

            )

        )

        conn.commit()

        print("\nContact Added Successfully.")

    except Error as err:

        print("\nUnable to Add Contact.")
        print(err)

    finally:

        if cursor:

            cursor.close()

        conn.close()


# =============================================================================
# FUNCTION NAME : view_contacts
#
# PURPOSE :
# Displays all contacts.
#
# =============================================================================

def view_contacts():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        cursor.execute(

            """

            SELECT

                c.contact_id,

                c.name,

                c.email,

                g.group_name

            FROM contacts c

            LEFT JOIN contact_groups g

            ON c.group_id = g.group_id

            ORDER BY c.name

            """

        )

        contacts = cursor.fetchall()

        print("\n===================================")
        print("           CONTACT LIST")
        print("===================================")

        if len(contacts) == 0:

            print("No Contacts Found.")

            return

        for row in contacts:

            print("-----------------------------------")
            print("Contact ID :", row[0])
            print("Name       :", row[1])
            print("Email      :", row[2])
            print("Group      :", row[3])

        print("-----------------------------------")

    except Error as err:

        print("\nUnable to Fetch Contacts.")
        print(err)

    finally:

        if cursor:

            cursor.close()

        conn.close()

# =============================================================================
# FUNCTION NAME : update_contact
#
# PURPOSE :
# Updates existing contact details.
#
# =============================================================================

def update_contact():

    conn = db_connection()

    if conn is None:

        return

    cursor = None

    try:

        cursor = conn.cursor(buffered=True)

        view_contacts()

        contact_id = input("\nEnter Contact ID : ").strip()

        if not contact_id.isdigit():

            print("Invalid Contact ID.")

            return


        cursor.execute(

            "SELECT * FROM contacts WHERE contact_id=%s",

            (contact_id,)

        )

        contact = cursor.fetchone()


        if contact is None:

            print("Contact Not Found.")

            return


        print("\nLeave blank to keep old value.")


        name = input(

            f"New Name [{contact[1]}] : "

        ).strip()


        email = input(

            f"New Email [{contact[2]}] : "

        ).strip()


        if name == "":

            name = contact[1]


        if email == "":

            email = contact[2]

        elif not check_email(email):

            print("Invalid Gmail Address.")

            return


        view_groups()


        group_id = input(

            "New Group ID : "

        ).strip()


        if group_id == "":

            group_id = contact[3]


        query = """

        UPDATE contacts

        SET

            name=%s,

            email=%s,

            group_id=%s

        WHERE contact_id=%s

        """


        cursor.execute(

            query,

            (

                name,

                email,

                group_id,

                contact_id

            )

        )


        conn.commit()


        print("\nContact Updated Successfully.")


    except Error as err:

        print("\nUpdate Error :")

        print(err)


    finally:

        if cursor:

            cursor.close()

        conn.close()



# =============================================================================
# FUNCTION NAME : delete_contact
#
# PURPOSE :
# Deletes a contact.
#
# =============================================================================

def delete_contact():

    conn = db_connection()

    if conn is None:

        return

    cursor = None


    try:

        cursor = conn.cursor(buffered=True)


        view_contacts()


        contact_id = input(

            "\nEnter Contact ID : "

        ).strip()


        if not contact_id.isdigit():

            print("Invalid Contact ID.")

            return


        cursor.execute(

            "SELECT contact_id FROM contacts WHERE contact_id=%s",

            (contact_id,)

        )


        if cursor.fetchone() is None:

            print("Contact Not Found.")

            return



        cursor.execute(

            "DELETE FROM contacts WHERE contact_id=%s",

            (contact_id,)

        )


        conn.commit()


        print("\nContact Deleted Successfully.")



    except Error as err:

        print("\nDelete Error :")

        print(err)


    finally:

        if cursor:

            cursor.close()

        conn.close()



# =============================================================================
# FUNCTION NAME : delete_group
#
# PURPOSE :
# Deletes contact group.
# Due to CASCADE, related contacts are also deleted.
#
# =============================================================================

def delete_group():

    conn = db_connection()

    if conn is None:

        return


    cursor = None


    try:

        cursor = conn.cursor(buffered=True)


        view_groups()


        group_id = input(

            "\nEnter Group ID : "

        ).strip()



        if not group_id.isdigit():

            print("Invalid Group ID.")

            return



        cursor.execute(

            "SELECT group_id FROM contact_groups WHERE group_id=%s",

            (group_id,)

        )


        if cursor.fetchone() is None:

            print("Group Not Found.")

            return



        cursor.execute(

            "DELETE FROM contact_groups WHERE group_id=%s",

            (group_id,)

        )


        conn.commit()


        print("\nGroup Deleted Successfully.")


    except Error as err:

        print("\nGroup Delete Error :")

        print(err)


    finally:

        if cursor:

            cursor.close()

        conn.close()



# =============================================================================
# FUNCTION NAME : menu
#
# PURPOSE :
# Displays contact management menu.
#
# =============================================================================

def menu():


    while True:


        print("\n===================================")

        print("       CONTACT MANAGEMENT SYSTEM")

        print("===================================")

        print("1. Create Group")

        print("2. View Groups")

        print("3. Add Contact")

        print("4. View Contacts")

        print("5. Update Contact")

        print("6. Delete Contact")

        print("7. Delete Group")

        print("8. Exit")

        print("===================================")


        choice = input("Enter Choice : ").strip()



        if choice == "1":

            create_group()



        elif choice == "2":

            view_groups()



        elif choice == "3":

            add_contact()



        elif choice == "4":

            view_contacts()



        elif choice == "5":

            update_contact()



        elif choice == "6":

            delete_contact()



        elif choice == "7":

            delete_group()



        elif choice == "8":

            print("\nReturning to Dashboard...")

            break



        else:

            print("\nInvalid Choice.")



# =============================================================================
# PROGRAM START
# =============================================================================

if __name__ == "__main__":


    create_tables()


    menu()