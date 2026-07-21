import datetime
from db import get_connection

def write_log(task, status, error="None"):
    conn, cursor = get_connection()
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sql = "INSERT INTO logs (time, task, status, error) VALUES (?,?,?,?)"
    values = (time, task, status, error)
    cursor.execute(sql, values)
    
    conn.commit()
    conn.close()
    print(f"[LOG] {task} - {status}")