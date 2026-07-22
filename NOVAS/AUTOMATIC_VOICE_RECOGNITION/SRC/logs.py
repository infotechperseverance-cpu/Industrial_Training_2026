# ============================================
# File Name : logs.py
# Description : Maintains Assistant Logs
# Author : Unnati Thakur
# ============================================

from database import get_connection


'''
@Function Name : add_log
@Description   : Stores user commands in log table
@Input Param   : module, command, status
@Output Param  : NONE
'''

def add_log(module, command, status):

    db = get_connection()

    if db is None:
        print("Unable to connect to the database.")
        return

    cur = None

    try:
        cur = db.cursor()

        cur.execute("""
            INSERT INTO logs(module, user_command, status)
            VALUES(%s,%s,%s)
        """, (module, command, status))

        db.commit()

    except Exception as e:
        print(f"Log Error: {e}")

    finally:
        if cur:
            cur.close()
        db.close()


'''
@Function Name : view_logs
@Description   : Displays all logs
@Input Param   : NONE
@Output Param  : NONE
'''

def view_logs():

    db = get_connection()

    if db is None:
        print("Unable to connect to the database.")
        return

    cur = None

    try:
        cur = db.cursor()

        cur.execute("""
            SELECT log_time, module, user_command, status
            FROM logs
            ORDER BY id DESC
        """)

        rows = cur.fetchall()

        print("\n========== LOG HISTORY ==========")

        if len(rows) == 0:
            print("No Logs Found.")
        else:
            for row in rows:
                print(f"""
Date & Time : {row[0]}
Module      : {row[1]}
Command     : {row[2]}
Status      : {row[3]}
--------------------------------------------
""")

    except Exception as e:
        print(f"Log Error: {e}")

    finally:
        if cur:
            cur.close()
        db.close()
        
'''
@Function Name : process_log_command
@Description   : Checks whether user wants to view logs
@Input Param   : command
@Output Param  : TRUE/FALSE
'''

def process(command):

    command = command.lower()

    keywords = [
        "show logs",
        "view logs",
        "display logs",
        "open logs",
        "i want to view logs",
        "show log",
        "view log"
    ]

    for keyword in keywords:

        if keyword in command:
            view_logs()
            return True

    return False
