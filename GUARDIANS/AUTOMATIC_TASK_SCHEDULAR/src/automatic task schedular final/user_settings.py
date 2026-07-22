import mysql.connector
import auth

def getconnection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="task_scheduler_db"
    )
    return connection
def view_profile():
    user = auth.get_current_user()
    if user is None: return
    conn = None
    cursor = None
    try:
        conn = getconnection()
        cursor = conn.cursor()
        query = "SELECT name, email, username, email_notifications, popup_notifications FROM users WHERE id = %s"
        cursor.execute(query, (user["id"],))
        result = cursor.fetchone()

        if result is not None:
            name, email, username, email_notif, popup_notif = result
            print("\n--- Your Profile ---")
            print(f"Name                  : {name}")
            print(f"Email                 : {email}")
            print(f"Username              : {username}")
            print(f"Email Notifications   : {'ON' if email_notif else 'OFF'}")
            print(f"Pop-up Notifications : {'ON' if popup_notif else 'OFF'}")
    except Exception as e:
        print("\n[!] Database Error: Profile settings disconnected.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
def edit_profile():
    user = auth.get_current_user()
    if user is None: return

    conn = None
    cursor = None
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, email FROM users WHERE id = %s", (user["id"],))
        record = cursor.fetchone()
        
        if record is None: return
        print("\nLeave blank to keep old values.")
        new_name = input(f"New Name [{record[0]}]: ").strip()
        new_email = input(f"New Email [{record[1]}]: ").strip()

        if new_name == "": new_name = record[0]
        if new_email == "": 
            new_email = record[1]
        else:
            if "@" not in new_email or "." not in new_email:
                print("Invalid email pattern.")
                return
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (new_name, new_email, user["id"]))
        conn.commit()
        user["name"] = new_name
        print("Profile details modified successfully.")
    except Exception as e:
        print("Error saving profile update details.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
def change_password():
    user = auth.get_current_user()
    if user is None: return

    conn = None
    cursor = None
    try:
        current_password = input("Current Password: ")
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE id = %s", (user["id"],))
        db_password = cursor.fetchone()
        if current_password != db_password[0]:
            print("Incorrect current password.")
            return

        new_password = input("New Password: ")
        confirm_new_password = input("Confirm New Password: ")

        if len(new_password) < 6:
            print("Error: Password should be >= 6 chars.")
            return
        if new_password != confirm_new_password:
            print("Passwords do not match.")
            return
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user["id"]))
        conn.commit()
        print("Password changed successfully.")
    except Exception as e:
        print("Error altering profile safety configs.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
def toggle_notifications():
    user = auth.get_current_user()
    if user is None: return

    conn = None
    cursor = None
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute("SELECT email_notifications, popup_notifications FROM users WHERE id = %s", (user["id"],))
        email_notif, popup_notif = cursor.fetchone()

        print(f"\nEmail Notifications: {'ON' if email_notif else 'OFF'}")
        choice = input("Toggle Email Notifications? (yes/no): ").strip().lower()
        if choice == "yes":
            cursor.execute("UPDATE users SET email_notifications = %s WHERE id = %s", (not email_notif, user["id"]))
        print(f"Pop-up Notifications: {'ON' if popup_notif else 'OFF'}")
        choice = input("Toggle Pop-up Notifications? (yes/no): ").strip().lower()
        if choice == "yes":
            cursor.execute("UPDATE users SET popup_notifications = %s WHERE id = %s", (not popup_notif, user["id"]))
        conn.commit()
        print("Notification configuration adjusted successfully.")
    except Exception as e:
        print("Error updating preferences.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
def settings_menu_flow():
    while True:
        print("\n--- User Settings ---")
        print("1. View Profile")
        print("2. Edit Profile")
        print("3. Change Password")
        print("4. Toggle Notifications")
        print("5. Back to Main Menu")        
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            view_profile()
        elif choice == "2":
            edit_profile()
        elif choice == "3":
            change_password()
        elif choice == "4":
            toggle_notifications()
        elif choice == "5":
            break
        else:
            print("Invalid select options.")