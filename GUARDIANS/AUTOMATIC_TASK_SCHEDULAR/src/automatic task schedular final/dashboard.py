import mysql.connector
from mysql.connector import Error
from datetime import datetime
import auth


def connect_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="task_scheduler_db"
        )

        if connection.is_connected():
            print("Database Connected Successfully")
            return connection

    except Error as e:
        print("Database Error:", e)
        return None


def get_dashboard_counts(cursor, user_id):
    try:

        today = datetime.now().date()

        # Total Tasks
        cursor.execute(
            "SELECT COUNT(*) AS total FROM tasks WHERE user_id=%s",
            (user_id,)
        )
        total = cursor.fetchone()["total"]

        # Complete Tasks
        cursor.execute(
            "SELECT COUNT(*) AS complete FROM tasks WHERE user_id=%s AND status='Complete'",
            (user_id,)
        )
        complete = cursor.fetchone()["complete"]

        # Pending Tasks
        cursor.execute(
            "SELECT COUNT(*) AS pending FROM tasks WHERE user_id=%s AND status='Pending' AND DATE(deadline)>=%s",
            (user_id, today)
        )
        pending = cursor.fetchone()["pending"]

        # Upcoming Tasks
        cursor.execute(
            """
            SELECT COUNT(*) AS upcoming
            FROM tasks
            WHERE user_id=%s
            AND DATE(deadline) > %s

            AND status='Pending'
            """,
            (user_id, today)
        )
        upcoming = cursor.fetchone()["upcoming"]

        # Overdue Tasks
        cursor.execute(
            """
            SELECT COUNT(*) AS overdue
            FROM tasks
            WHERE user_id=%s
            AND DATE(deadline) < %s
            AND status!='Complete'
            """,
            (user_id, today)
        )
        overdue = cursor.fetchone()["overdue"]

        print("\n========== DASHBOARD ==========")
        print("Total Tasks      :", total)
        print("Completed Tasks  :", complete)
        print("Pending Tasks    :", pending)
        print("Upcoming Tasks   :", upcoming)
        print("Overdue Tasks    :", overdue)

    except Error as e:
        print("Dashboard Error :", e)


if __name__ == "__main__":

    # ensure user logs in via auth gate menu (no manual User ID prompt)
    proceed = auth.login_gate_menu()
    if not proceed:
        print("Exiting.")
    else:
        connection = connect_database()

        if connection:

            cursor = connection.cursor(dictionary=True)

            user_id = auth.get_user_id()
            if user_id is None:
                print("User not logged in. Exiting.")
            else:
                get_dashboard_counts(cursor, user_id)

            cursor.close()
            connection.close()
