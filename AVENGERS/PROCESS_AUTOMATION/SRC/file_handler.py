import os
import datetime

from db import get_connection
from logger import write_log


# ==========================================
# SAVE FILE OPERATION TO DATABASE
# ==========================================

def save_file_log(filename, action, content):

    conn, cursor = get_connection()

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO file_log
        (file_name, action, content, time)
        VALUES (?, ?, ?, ?)
    """,
    (
        filename,
        action,
        content,
        current_time
    ))

    conn.commit()
    conn.close()


# ==========================================
# WRITE FILE
# ==========================================

def write_file(filename, data):

    try:

        with open(filename, "w", encoding="utf-8") as file:

            file.write(data)

        save_file_log(
            filename,
            "WRITE",
            data
        )

        write_log(
            "Write File",
            "Success"
        )

        print("\nFile Written Successfully.")

    except Exception as e:

        print(e)

        write_log(
            "Write File",
            "Failure",
            str(e)
        )


# ==========================================
# READ FILE
# ==========================================

def read_file(filename):

    try:

        if not os.path.exists(filename):

            print("File Does Not Exist.")
            return

        with open(filename, "r", encoding="utf-8") as file:

            data = file.read()

        save_file_log(
            filename,
            "READ",
            data
        )

        write_log(
            "Read File",
            "Success"
        )

        print("\n========== FILE CONTENT ==========\n")
        print(data)

    except Exception as e:

        print(e)

        write_log(
            "Read File",
            "Failure",
            str(e))


# ==========================================
# APPEND FILE
# ==========================================

def append_file(filename, data):

    try:

        with open(filename, "a", encoding="utf-8") as file:

            file.write(data + "\n")

        save_file_log(
            filename,
            "APPEND",
            data
        )

        write_log(
            "Append File",
            "Success"
        )

        print("\nData Appended Successfully.")

    except Exception as e:

        print(e)

        write_log(
            "Append File",
            "Failure",
            str(e))

# ==========================================
# VIEW FILE LOGS
# ==========================================

def show_file_logs():

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT
            id,
            file_name,
            action,
            time
        FROM file_log
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    print("\n========== FILE LOGS ==========")

    if len(records) == 0:

        print("No File Logs Found.")

    else:

        for record in records:

            print(f"""
Log ID        : {record[0]}
File Name     : {record[1]}
Action        : {record[2]}
Time          : {record[3]}
----------------------------------------
""")

    conn.close()


# ==========================================
# DELETE FILE LOG
# ==========================================

def delete_file_log(log_id):

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT *
        FROM file_log
        WHERE id=?
    """, (log_id,))

    if cursor.fetchone() is None:

        print("File Log Not Found.")
        conn.close()
        return

    try:

        cursor.execute("""
            DELETE FROM file_log
            WHERE id=?
        """, (log_id,))

        conn.commit()

        print("\nFile Log Deleted Successfully.")

        write_log(
            "Delete File Log",
            "Success"
        )

    except Exception as e:

        print(e)

        write_log(
            "Delete File Log",
            "Failure",
            str(e)
        )

    finally:

        conn.close()


# ==========================================
# FILE HANDLER MENU
# ==========================================

def file_handler_menu():

    while True:

        print("\n========== FILE HANDLER ==========")
        print("1. Write File")
        print("2. Read File")
        print("3. Append File")
        print("4. View File Logs")
        print("5. Delete File Log")
        print("6. Back")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            filename = input("File Name : ")
            data = input("Enter Data : ")

            write_file(filename, data)

        elif choice == "2":

            filename = input("File Name : ")

            read_file(filename)

        elif choice == "3":

            filename = input("File Name : ")
            data = input("Enter Data : ")

            append_file(filename, data)

        elif choice == "4":

            show_file_logs()

        elif choice == "5":

            try:
                log_id = int(input("Log ID : "))
                delete_file_log(log_id)
            except ValueError:
                print("Invalid Log ID.")

        elif choice == "6":

            break

        else:

            print("Invalid Choice.")


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    file_handler_menu()