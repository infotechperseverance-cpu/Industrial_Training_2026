import db
import auth

conn = db.getconnection()
cursor = conn.cursor(dictionary=True)


def delete_task(task_id, user_id):
    copy = "INSERT IGNORE INTO recycle_bin SELECT * FROM tasks WHERE id=%s AND user_id=%s"
    cursor.execute(copy, (task_id, user_id))

    query = "DELETE FROM tasks WHERE id=%s AND user_id=%s"
    cursor.execute(query, (task_id, user_id))
    conn.commit()
    print("task deleted successfully")


def view_deleted_task(user_id):
    show = "select * FROM recycle_bin WHERE user_id=%s"
    cursor.execute(show, (user_id,))
    deleted_task = cursor.fetchall()
    if not deleted_task:
        print("no deleted task")
        return
    for task in deleted_task:
        print(task)


def restore_task(task_id, user_id):
    restore = "INSERT IGNORE INTO tasks SELECT * FROM recycle_bin WHERE id=%s AND user_id=%s"
    cursor.execute(restore, (task_id, user_id))
    conn.commit()
    delete = "DELETE FROM recycle_bin WHERE id=%s AND user_id=%s"
    cursor.execute(delete, (task_id, user_id))
    conn.commit()
    print("restored succesfully")


def validate_id(task_id, user_id):
    try:
        tid = int(task_id)
    except ValueError:
        print("invaild task_id,task not found")
        return False

    check_query = "SELECT * FROM tasks WHERE id=%s AND user_id=%s"
    cursor.execute(check_query, (tid, user_id))
    task = cursor.fetchone()
    if task is None:
        print("invaild task_id,task not found")
        return False
    return True


def validate_recyclebinid(task_id, user_id):
    try:
        tid = int(task_id)
    except ValueError:
        print("invaild task_id,task not found")
        return False

    check_query = "SELECT * FROM recycle_bin WHERE id=%s AND user_id=%s"
    cursor.execute(check_query, (tid, user_id))
    task = cursor.fetchone()
    if task is None:
        print("invaild task_id,task not found")
        return False
    return True


def delete_task_permanently(task_id, user_id):
    delete = "DELETE FROM recycle_bin WHERE id=%s AND user_id=%s"
    cursor.execute(delete, (task_id, user_id))
    conn.commit()
    print("task deleted permently")


if __name__ == "__main__":

    proceed = auth.login_gate_menu()
    if not proceed:
        print("Exiting....")
    else:
        user_id = auth.get_user_id()
        if user_id is None:
            print("No user logged in. Exiting....")
        else:
            # ensure user_id is int
            try:
                user_id = int(user_id)
            except Exception:
                pass

            while True:

                print("\n========== RECYCLE BIN ==========")
                print("1.delete task")
                print("2.view deleted task")
                print("3.Restore a task")
                print("4.permanently delete the task")
                print("5.Back to main menu")
                try:
                    option = int(input("enter your choice:"))
                except ValueError:
                    print("please enter valid number")
                    continue
                match option:
                    case 1:
                        task_id = input("Enter task_id:")
                        if validate_id(task_id, user_id):
                            delete_task(int(task_id), user_id)
                    case 2:
                        view_deleted_task(user_id)
                    case 3:
                        task_id = input("Enter task_id:")
                        if validate_recyclebinid(task_id, user_id):
                            restore_task(int(task_id), user_id)
                    case 4:
                        task_id = input("Enter task_id:")
                        if validate_recyclebinid(task_id, user_id):
                            delete_task_permanently(int(task_id), user_id)
                    case 5:
                        cursor.close()
                        conn.close()
                        print("Exiting....")
                        break
                    case _:
                        print("Invalid choice! Please select again.")
