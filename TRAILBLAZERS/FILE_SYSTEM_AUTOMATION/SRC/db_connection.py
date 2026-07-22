
import mysql.connector


def get_connection():

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="12345",
        database="File_System_Automation"
    )

    return connection
