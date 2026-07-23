import datetime

from db import get_connection
from logger import write_log
from process import execute_process


# ==========================================
# RUN AUTOMATIC TASK
# ==========================================

def automatic_task(process_id):

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT process_name
        FROM processes
        WHERE process_id=?
    """, (process_id,))

    process = cursor.fetchone()

    if process is None:

        print("Process Not Found.")
        conn.close()
        return

    process_name = process[0]

    execution_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:

        print(f"\nRunning Automation : {process_name}")

        execute_process(process_id)

        cursor.execute("""
            INSERT INTO task_log
            (task_name, status, execution_time)
            VALUES (?, ?, ?)
        """,
        (
            process_name,
            "Success",
            execution_time
        ))

        conn.commit()

        print("Automation Completed Successfully.")

        write_log(
            "Automatic Task",
            "Success"
        )

    except Exception as e:

        cursor.execute("""
            INSERT INTO task_log
            (task_name, status, execution_time)
            VALUES (?, ?, ?)
        """,
        (
            process_name,
            f"Failed : {e}",
            execution_time
        ))

        conn.commit()

        print("Automation Failed.")

        write_log(
            "Automatic Task",
            "Failure",
            str(e)
        )

    finally:

        conn.close()


# ==========================================
# VIEW AUTOMATION HISTORY
# ==========================================

def show_automation_history():

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT
            id,
            task_name,
            status,
            execution_time
        FROM task_log
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    print("\n========== AUTOMATION HISTORY ==========")

    if len(records) == 0:

        print("No Automation Records Found.")

    else:

        for record in records:

            print(f"""
Automation ID : {record[0]}
Task Name     : {record[1]}
Status        : {record[2]}
Executed At   : {record[3]}
----------------------------------------
""")

    conn.close()

# ==========================================
# DELETE AUTOMATION RECORD
# ==========================================

def delete_automation_record(record_id):

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT *
        FROM task_log
        WHERE id=?
    """, (record_id,))

    if cursor.fetchone() is None:

        print("Automation Record Not Found.")
        conn.close()
        return

    try:

        cursor.execute("""
            DELETE FROM task_log
            WHERE id=?
        """, (record_id,))

        conn.commit()

        print("\nAutomation Record Deleted Successfully.")

        write_log(
            "Delete Automation Record",
            "Success"
        )

    except Exception as e:

        print(e)

        write_log(
            "Delete Automation Record",
            "Failure",
            str(e)
        )

    finally:

        conn.close()


# ==========================================
# CLEAR AUTOMATION HISTORY
# ==========================================

def clear_automation_history():

    conn, cursor = get_connection()

    choice = input(
        "Are you sure you want to clear all automation history? (yes/no): "
    )

    if choice.lower() != "yes":

        print("Operation Cancelled.")
        conn.close()
        return

    try:

        cursor.execute("DELETE FROM task_log")

        conn.commit()

        print("\nAutomation History Cleared Successfully.")

        write_log(
            "Clear Automation History",
            "Success"
        )

    except Exception as e:

        print(e)

        write_log(
            "Clear Automation History",
            "Failure",
            str(e)
        )

    finally:

        conn.close()


# ==========================================
# AUTOMATION MENU
# ==========================================

def automation_menu():

    while True:

        print("\n========== AUTOMATION ==========")
        print("1. Run Automatic Task")
        print("2. View Automation History")
        print("3. Delete Automation Record")
        print("4. Clear Automation History")
        print("5. Back")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            try:
                process_id = int(input("Process ID : "))
                automatic_task(process_id)
            except ValueError:
                print("Invalid Process ID.")

        elif choice == "2":

            show_automation_history()

        elif choice == "3":

            try:
                record_id = int(input("Automation Record ID : "))
                delete_automation_record(record_id)
            except ValueError:
                print("Invalid Record ID.")

        elif choice == "4":

            clear_automation_history()

        elif choice == "5":

            break

        else:

            print("Invalid Choice.")


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    automation_menu()