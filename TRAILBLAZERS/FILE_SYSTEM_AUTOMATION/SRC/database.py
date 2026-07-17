import pymysql
from pymysql import MySQLError

# ==============================
# Database Configuration
# ==============================

HOST = "localhost"
USER = "root"
PASSWORD = "root02"      
DATABASE = "file_management"

# ==============================
# Create Database
# ==============================

def create_database():
    try:
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        connection.commit()

        cursor.close()
        connection.close()

    except MySQLError as e:
        print("Database Creation Error:", e)

# ==============================
# Get Connection
# ==============================

def get_connection():
    create_database()

    try:
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            cursorclass=pymysql.cursors.DictCursor
        )

        return connection

    except MySQLError as e:
        print("Connection Error:", e)
        return None

# ==============================
# Execute INSERT / UPDATE / DELETE
# ==============================

def execute_query(query, values=None):
    connection = get_connection()

    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()

        except MySQLError as e:
            print("Query Error:", e)

        finally:
            cursor.close()
            connection.close()

# ==============================
# Fetch Multiple Records
# ==============================

def fetch_all(query, values=None):
    connection = get_connection()

    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, values)
            return cursor.fetchall()

        except MySQLError as e:
            print("Fetch Error:", e)

        finally:
            cursor.close()
            connection.close()

    return []

# ==============================
# Fetch Single Record
# ==============================

def fetch_one(query, values=None):
    connection = get_connection()

    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, values)
            return cursor.fetchone()

        except MySQLError as e:
            print("Fetch Error:", e)

        finally:
            cursor.close()
            connection.close()

    return None