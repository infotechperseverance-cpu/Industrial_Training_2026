import mysql.connector
from mysql.connector import Error

def connect_database():
    try:
        con=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pass@123",
            database="bulk_email_system"
        )
        print("Database Connected Successfully")
        return con
    except Error as e:
        print("Database Error:",e)
        return None

def create_tables(con):
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS contact_groups(
        group_id INT AUTO_INCREMENT PRIMARY KEY,
        group_name VARCHAR(100) UNIQUE NOT NULL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS contacts(
        contact_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(150) UNIQUE,
        group_id INT,
        FOREIGN KEY(group_id) REFERENCES contact_groups(group_id)
        ON DELETE CASCADE)""")
    con.commit(); cur.close()

def create_group(con):
    cur=con.cursor()
    name=input("Group Name: ")
    try:
        cur.execute("INSERT INTO contact_groups(group_name) VALUES(%s)",(name,))
        con.commit(); print("Group Created.")
    except Error as e:
        print(e)
    cur.close()

def view_groups(con):
    cur=con.cursor()
    cur.execute("SELECT * FROM contact_groups")
    rows=cur.fetchall()
    for r in rows:
        print(r)
    if not rows: print("No groups.")
    cur.close()

def add_contact(con):
    cur=con.cursor()
    name=input("Name: ")
    email=input("Email: ")
    view_groups(con)
    gid=input("Group ID: ")
    try:
        cur.execute("INSERT INTO contacts(name,email,group_id) VALUES(%s,%s,%s)",(name,email,gid))
        con.commit(); print("Contact Added.")
    except Error as e:
        print(e)
    cur.close()

def view_contacts(con):
    cur=con.cursor()
    cur.execute("""SELECT c.contact_id,c.name,c.email,g.group_name
                   FROM contacts c JOIN contact_groups g
                   ON c.group_id=g.group_id""")
    rows=cur.fetchall()
    for r in rows:
        print(r)
    if not rows: print("No contacts.")
    cur.close()


def update_contact(con):
    cur=con.cursor()
    cid=input("Contact ID: ")
    name=input("New Name: ")
    email=input("New Email: ")
    view_groups(con)
    gid=input("New Group ID: ")
    cur.execute("UPDATE contacts SET name=%s,email=%s,group_id=%s WHERE contact_id=%s",
                (name,email,gid,cid))
    con.commit()
    print("Updated.")
    cur.close()

def delete_contact(con):
    cur=con.cursor()
    cid=input("Contact ID: ")
    cur.execute("DELETE FROM contacts WHERE contact_id=%s",(cid,))
    con.commit()
    print("Deleted.")
    cur.close()

def delete_group(con):
    cur=con.cursor()
    view_groups(con)
    gid=input("Group ID: ")
    cur.execute("DELETE FROM contact_groups WHERE group_id=%s",(gid,))
    con.commit()
    print("Group Deleted.")
    cur.close()

def menu():
    print("""
1.Create Group
2.View Groups
3.Add Contact
4.View Contacts
5.Update Contact
6.Delete Contact
7.Delete Group
8.Exit
""")

if __name__=="__main__":
    con=connect_database()
    if con:
        create_tables(con)
        while True:
            menu()
            ch=input("Choice: ")
            if ch=="1": create_group(con)
            elif ch=="2": view_groups(con)
            elif ch=="3": add_contact(con)
            elif ch=="4": view_contacts(con)
            elif ch=="5": update_contact(con)
            elif ch=="6": delete_contact(con)
            elif ch=="7": delete_group(con)
            elif ch=="8": break
            else: print("Invalid Choice")
        con.close()
