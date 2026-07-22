
import auth
from datetime import datetime, timedelta
from mysql.connector import Error

def connect_database():
    try:
        conn = auth.getconnection()
        if conn is not None and conn.is_connected():

            return conn
    except Error as e:
        print("Database Error:", e)
    return None

def show_calendar(cursor=None):
    user_id = auth.get_user_id()
    if user_id is None:
        print("No user logged in. Please login or register first.")
        return

    created_cursor = False
    if cursor is None:
        conn = connect_database()
        if conn is None:
            print("Unable to connect to database.")
            return
        cursor = conn.cursor(dictionary=True)
        created_cursor = True

    try:
        while True:

            print("\n--- Calendar View ---")
            print("1. View by Month")
            print("2. View by Week")
            print("3. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                view_by_month(cursor, user_id)

            elif choice == "2":
                view_by_week(cursor, user_id)

            elif choice == "3":
                print("Returning to Main Menu...")
                return

            else:
                print("Invalid choice.")

    finally:
        if created_cursor:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

def view_by_month(cursor, user_id):
    month = input("Enter Month (YYYY-MM): ")

    try:
        year, mon = month.split("-")
        start_date = f"{month}-01"

        if int(mon) == 12:
            end_date = f"{int(year)+1}-01-01"
        else:
            end_date = f"{year}-{int(mon)+1:02d}-01"

        query = """
        SELECT *
        FROM tasks
        WHERE user_id=%s
        AND deadline >= %s
        AND deadline < %s
        ORDER BY deadline
        """

        cursor.execute(
            query,
            (user_id, start_date, end_date)
        )

        result = cursor.fetchall()

        print(f"\n--- {datetime.strptime(month,'%Y-%m').strftime('%B %Y')} ---")

        if len(result)==0:
            print("No Tasks Found.")
            return

        for task in result:
            # preserve original print style exactly as before
            print(
                task["deadline"].day,
                ":",
                task["title"],
                "(",
                task["status"],
                ")"
            )

    except ValueError:
        print("Invalid Month Format.")

def view_by_week(cursor, user_id):
    start = input("Enter Week Start Date (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(start,"%Y-%m-%d")
        end_date = start_date + timedelta(days=6)

        query = """
        SELECT *
        FROM tasks
        WHERE user_id=%s
        AND DATE(deadline) BETWEEN %s AND %s
        ORDER BY deadline
        """

        cursor.execute(
            query,
            (
                user_id,
                start_date.date(),
                end_date.date()
            )
        )

        result = cursor.fetchall()

        print(f"\n--- Week of {start} ---")

        if len(result)==0:
            print("No Tasks Found.")
            return

        for task in result:
            day = task["deadline"].strftime("%a %d")
            # preserve original print style exactly as before
            print(
                day,
                ":",
                task["title"],
                "(",
                task["status"],
                ")"
            )

    except ValueError:
        print("Invalid Date Format.")

if __name__ == "__main__":
    proceed = auth.login_gate_menu()
    if not proceed:
        print("Exiting.")
    else:
        connection = connect_database()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                show_calendar(cursor)
            finally:
                cursor.close()
                connection.close()
