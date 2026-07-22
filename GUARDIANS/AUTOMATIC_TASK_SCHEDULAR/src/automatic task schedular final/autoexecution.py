import db
import time
from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_incomplete_tasks():
    try:
        connection = db.getconnection()
        cursor = connection.cursor()
        query = "SELECT id,user_id,deadline FROM tasks WHERE status = 'pending' "
        cursor.execute(query)
        tasks = cursor.fetchall()
        for task in tasks:
            id = task[0]
            user_id = task[1]
            deadline = task[2]
            if deadline < datetime.now():
                update = " UPDATE tasks SET status='overdue' WHERE id=%s AND user_id=%s"

                cursor.execute(update, (id, user_id))
                connection.commit()

                print("task id:", id, "is overdue ")

    except Exception as e:
        print("error:", e)
    finally:
        cursor.close()
        connection.close()


while True:
    check_incomplete_tasks()
    time.sleep(1)