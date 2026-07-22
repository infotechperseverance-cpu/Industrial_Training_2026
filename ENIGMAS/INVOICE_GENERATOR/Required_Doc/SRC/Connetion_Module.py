import mysql.connector
from mysql.connector.aio import cursor

""" function-1 name : connection: which make connection return connection object 
                      it invoice_generator database
                      input parameters: none(make change in connection fn enter password,username)
                      output parameters: connection object
                      
    function-2 name: create_tables :  it makes all required tables for invoice generator
                                     input parameters : none
                                     output parameters: none                    
"""
# Connection
def connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234"
        )

        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS invoice_generator")

        cursor.close()
        conn.close()

        # Connect to the created database
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="invoice_generator"
        )
    except Exception as e:
        print("Connection error:", e)
        return None

#create tables function
def create_tables():
    try:
        conn = connection()
        cursor = conn.cursor()

       #users table
        # users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            counter_no INT NOT NULL
        )
        """)

        default_users = [
            ("counter1", "admin123", 1),
            ("counter2", "admin123", 2),
            ("counter3", "admin123", 3),
            ("counter4", "admin123", 4),
            ("counter5", "admin123", 5),
            ("counter6", "admin123", 6),
        ]

        cursor.executemany("""
        INSERT IGNORE INTO users (username, password, counter_no)
        VALUES (%s, %s, %s)
        """, default_users)
                

       #customers table
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS customers (customer_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL, mobile_no VARCHAR(15) NOT NULL, email VARCHAR(100) NOT NULL)""")
        #products table
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS products (product_id INT AUTO_INCREMENT PRIMARY KEY, 
            product_name VARCHAR(100) NOT NULL, category VARCHAR(50) NOT NULL,
                price DECIMAL(10,2) NOT NULL, gst_percent DECIMAL(5,2) NOT NULL, stock_quantity INT NOT NULL)""")
        #invoice table
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS invoices (invoice_id INT AUTO_INCREMENT PRIMARY KEY, customer_id INT NOT NULL,
                user_id INT NOT NULL, invoice_date DATE NOT NULL, subtotal DECIMAL(10,2) NOT NULL, 
                gst_amount DECIMAL(10,2) NOT NULL, discount DECIMAL(10,2), total_amount DECIMAL(10,2) NOT NULL,
                pdf_path VARCHAR(255), email_status VARCHAR(20), FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY(user_id) REFERENCES users(user_id))""")
        #invoice_items table
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS invoice_items (item_id INT AUTO_INCREMENT PRIMARY KEY, 
                invoice_id INT NOT NULL, product_id INT NOT NULL, quantity INT NOT NULL, 
                unit_price DECIMAL(10,2) NOT NULL, gst_amount DECIMAL(10,2) NOT NULL, 
                total_price DECIMAL(10,2) NOT NULL, FOREIGN KEY(invoice_id) REFERENCES invoices(invoice_id),
                FOREIGN KEY(product_id) REFERENCES products(product_id))""")
        # returns table
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS returns (return_id INT AUTO_INCREMENT PRIMARY KEY, invoice_id INT NOT NULL, 
                product_id INT NOT NULL, quantity INT NOT NULL, return_date DATE NOT NULL, return_reason VARCHAR(255) NOT NULL,
                FOREIGN KEY(invoice_id) REFERENCES invoices(invoice_id), FOREIGN KEY(product_id) REFERENCES products(product_id))""")


        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("something went wrong")
        return None

