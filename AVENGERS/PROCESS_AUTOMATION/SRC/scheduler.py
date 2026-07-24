import schedule
import time
import datetime

from db import get_connection
from logger import write_log


# ==========================================
# SCHEDULE A TASK
# ==========================================

def schedule_task(task_name, interval):

    conn, cursor = get_connection()

    try:

        cursor.execute("""
            SELECT *
            FROM schedule_log
            WHERE task_name=?
        """, (task_name,))

        if cursor.fetchone():

            print("Task is already scheduled.")
            conn.close()
            return

        cursor.execute("""
            INSERT INTO schedule_log
            (task_name, schedule_time, last_run)
            VALUES (?, ?, ?)
        """, (
            task_name,
            f"Every {interval} Seconds",
            "Not Executed"
        ))

        conn.commit()

        schedule.every(interval).seconds.do(run_task, task_name)

        print("\nTask Scheduled Successfully.")

        write_log(
            "Schedule Task",
            "Success"
        )

    except Exception as e:

        print(e)

        write_log(
            "Schedule Task",
            "Failure",
            str(e)
        )

    finally:

        conn.close()


# ==========================================
# RUN SCHEDULED TASK
# ==========================================

def run_task(task_name):

    conn, cursor = get_connection()

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:

        print(f"\nRunning Task : {task_name}")

        cursor.execute("""
            UPDATE schedule_log
            SET last_run=?
            WHERE task_name=?
        """, (
            current_time,
            task_name
        ))

        conn.commit()

        write_log(
            f"Scheduled Task : {task_name}",
            "Success"
        )

    except Exception as e:

        write_log(
            f"Scheduled Task : {task_name}",
            "Failure",
            str(e)
        )

    finally:

        conn.close()


# ==========================================
# START SCHEDULER
# ==========================================

def start_scheduler():

    print("\nScheduler Started...")
    print("Press Ctrl + C to stop.\n")

    while True:

        schedule.run_pending()
        time.sleep(1)

# ==========================================
# VIEW SCHEDULED TASKS
# ==========================================

def show_scheduled_tasks():

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT
            id,
            task_name,
            schedule_time,
            last_run
        FROM schedule_log
        ORDER BY id
    """)

    tasks = cursor.fetchall()

    print("\n========== SCHEDULED TASKS ==========")

    if len(tasks) == 0:

        print("No Scheduled Tasks Found.")

    else:

        for task in tasks:

            print(f"""
Schedule ID    : {task[0]}
Task Name      : {task[1]}
Schedule       : {task[2]}
Last Run       : {task[3]}
----------------------------------------
""")

    conn.close()


# ==========================================
# DELETE SCHEDULED TASK
# ==========================================

def delete_scheduled_task(schedule_id):

    conn, cursor = get_connection()

    cursor.execute("""
        SELECT *
        FROM schedule_log
        WHERE id=?
    """, (schedule_id,))

    if cursor.fetchone() is None:

        print("Scheduled Task Not Found.")
        conn.close()
        return

    try:

        cursor.execute("""
            DELETE FROM schedule_log
            WHERE id=?
        """, (schedule_id,))

        conn.commit()

        print("\nScheduled Task Deleted Successfully.")

        write_log(
            "Delete Scheduled Task",
            "Success"
        )

    except Exception as e:

        print(e)

        write_log(
            "Delete Scheduled Task",
            "Failure",
            str(e)
        )

    finally:

        conn.close()


# ==========================================
# SCHEDULER MENU
# ==========================================

def scheduler_menu():

    while True:

        print("\n========== TASK SCHEDULER ==========")
        print("1. Schedule New Task")
        print("2. View Scheduled Tasks")
        print("3. Delete Scheduled Task")
        print("4. Start Scheduler")
        print("5. Back")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            task_name = input("Task Name : ")

            try:
                interval = int(input("Run Every (Seconds) : "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            schedule_task(task_name, interval)

        elif choice == "2":

            show_scheduled_tasks()

        elif choice == "3":

            try:
                schedule_id = int(input("Schedule ID : "))
            except ValueError:
                print("Invalid Schedule ID.")
                continue

            delete_scheduled_task(schedule_id)

        elif choice == "4":

            start_scheduler()

        elif choice == "5":

            break

        else:

            print("Invalid Choice.")


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    scheduler_menu()