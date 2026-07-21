'''
@Module Name : database.py

@Description : Establishes and returns a MySQL database
               connection for the NOVA project.

@Author      : Bhoomi Sapke
'''

import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def get_connection():
   

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            use_pure=True
        )

        return connection

    except Error as e:
        print(f"Database Connection Error: {e}")
        return None