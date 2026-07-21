from Connetion_Module import connection

conn = connection()
cursor = conn.cursor()

cursor.execute("SELECT user_id, username, counter_no FROM users")

rows = cursor.fetchall()

if not rows:
    print("No users found.")
else:
    for row in rows:
        print(row)

cursor.close()
conn.close()