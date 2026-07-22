import db
conn=db.getconnection()
cursor=conn.cursor()

def delete_task():
  task_id= input("enter task _id to delete:")
  copy="INSERT IGNORE INTO recycle_bin SELECT* FROM tasks WHERE id=%s"
  cursor.execute(copy,(task_id,))
  
  
  query="DELETE FROM tasks WHERE id=%s"
  cursor.execute(query,(task_id,))
  conn.commit()
  print("task deleted successfully")


def view_deleted_task():
   show="select * FROM recycle_bin"
   cursor.execute(show)
   deleted_task=cursor.fetchall()
   for task in deleted_task:
      print(task)

def restore_task():
   
 task_id=input(print("enter task id"))

   
 restore="INSERT IGNORE INTO tasks SELECT* FROM recycle_bin WHERE id=%s"
 cursor.execute(restore,(task_id,))
 conn.commit()
 delete="DELETE FROM recycle_bin WHERE id=%s"
 cursor.execute(delete,(task_id,))
 conn.commit()
 print("restored succesfully")

def delete_task_permently():
 task_id= input("enter task id:")

 delete="DELETE FROM recycle_bin WHERE id=%s"
 cursor.execute(delete,(task_id,))
 conn.commit()
 print("task deleted permently")




        
while True:
 print("*Recycle bin*")
 print("1.delete task")
 print("2.view deleted task")
 print("3.Restore a task")
 print("4.permanently delete the task")
 print("5.Back to main menu")

 option= int(input("enter your choice:"))
 match option:
    case 1:
       delete_task()
       break
    case 2:
        view_deleted_task()
        break
        
    case 3:
        restore_task()
        break
    case 4:
        delete_task_permently()
        break
    case _:
        print("exiting....")
        break

