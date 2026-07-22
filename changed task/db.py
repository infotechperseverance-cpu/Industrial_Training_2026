import mysql.connector

def getconnection():
    connection =mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="task_scheduler_db"
    )
    return connection

conn=getconnection()
cursor=conn.cursor()
def insert_task(task_data):
    insert_query = "INSERT INTO tasks(user_id, title, description, tag, deadline, recurring,priority,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, task_data)
    conn.commit()
    print("Task inserted successfully.")
def show_tasks(user_id):
 cursor.execute("SELECT * FROM tasks WHERE user_id=%s ORDER BY deadline ASC",(user_id,))
 tasks = cursor.fetchall()
 for task in tasks:
        print(task)
 print("Tasks displayed successfully.")
conn.commit()

def filter_tasks(criteria):
   filter_query="SELECT * FROM tasks WHERE priority=%s"
   cursor.execute(filter_query, (criteria,))
   tasks=cursor.fetchall()
   return tasks

def update_task(task_data):
    update_query="UPDATE tasks SET title=%s, description=%s, tag=%s, deadline=%s, priority=%s, status=%s, recurring=%s WHERE user_id=%s"
    cursor.execute(update_query, task_data)
    conn.commit()
    print("Task updated successfully.")
def delete_task(id,user_id):
    copy_data="INSERT INTO recycle_bin SELECT * FROM tasks WHERE id = %s AND user_id=%s"
    cursor.execute(copy_data, (id, user_id))
    delete_query = "DELETE FROM tasks WHERE id = %s AND user_id=%s"
    cursor.execute(delete_query, (id, user_id))
    conn.commit()
    print("Task deleted successfully.")
def restore_task(id,user_id):
    restore_query = "INSERT INTO tasks SELECT * FROM recycle_bin WHERE id = %s AND user_id=%s"
    cursor.execute(restore_query, (id,user_id))
    conn.commit()
    delete_query = "DELETE FROM recycle_bin WHERE id = %s AND user_id=%s"
    cursor.execute(delete_query, (id, user_id))
    conn.commit()
    print("Task restored successfully.")