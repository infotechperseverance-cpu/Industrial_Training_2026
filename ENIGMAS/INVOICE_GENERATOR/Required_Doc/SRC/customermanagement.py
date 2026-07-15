import sqlite3

conn = sqlite3.connect("customer.db")
cur =  conn.cursor()


'''
@Function Name : create_table
@Description   : This function creates the customer table in the database.
                 If the table is already present, it will not create it again.
@Input Param   : NONE
@Output Param  : NONE
@Author        : Prashik Dabhade
'''        
def create_table():
        cur.execute("""
        CREATE TABLE IF NOT EXISTS customer(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mobile TEXT,
            email TEXT
        )
        """)
        conn.commit()

'''
@Function Name : add_customer
@Description   : This function takes customer name, mobile number and email
                 from the user and saves the details into the database.
@Input Param   : NONE (User Input)
                 Name
                 Mobile Number
                 Email
@Output Param  : NONE
@Author        : Prashik Dabhade
'''

def add_customer():
    name = input("Enter Customer Name: ")
    mobile = input("Enter Mobile Number: ")
    email = input("Enter Email: ")

    cur.execute(
        "INSERT INTO customer(name,mobile,email) VALUES(?,?,?)",
        (name, mobile, email)
        )
    conn.commit()
    print("Customer Added Successfully!")
    

'''
@Function Name : search_customer
@Description   : This function asks the user to search a customer by
                 name or mobile number. If the customer is found,
                 it displays the customer details.
@Input Param   : NONE (User Input)
                 Search Choice
                 Name or Mobile Number
@Output Param  : NONE
@Author        : Prashik Dabhade
'''
def search_customer():

    choice = input("Search by (1-Name / 2-Mobile): ")

    if choice == "1":
        name = input("Enter Customer Name: ")
        cur.execute(
            "SELECT * FROM customer WHERE name=?",
                (name,)
                )
        
    elif choice == "2":
        mobile = input("Enter Mobile Number: ")
        cur.execute(
            "SELECT * FROM customer WHERE mobile=?",
            (mobile,)
            )
        
    else:
        print("Invalid Choice!")
        return

    customer = cur.fetchall()

    if customer:
        for data in customer:
        
            print("\nCustomer Found")
            print("ID:", data[0])
            print("Name:", data[1])
            print("Mobile:", data[2])
            print("Email:", data[3])
            
    else:
        print("Customer Not Found!")
        

'''
@Function Name : update_customer
@Description   : This function finds a customer using the mobile number.
                 If the customer exists, it updates the customer's
                 name and email address.
@Input Param   : NONE (User Input)
                 Mobile Number
                 New Name
                 New Email
@Output Param  : NONE
@Author        : Prashik Dabhade
'''
def update_customer():
    mobile = input("Enter Mobile Number of Customer: ")

    cur.execute(
            "SELECT * FROM customer WHERE mobile=?",
            (mobile,)
        )

    if cur.fetchone():
        name = input("Enter New Name: ")
        email = input("Enter New Email: ")

        cur.execute(
            "UPDATE customer SET name=?, email=? WHERE mobile=?",
            (name, email, mobile)
        )
        conn.commit()

        print("Customer Updated Successfully!")
        
    else:
        print("Customer Not Found!")

'''
@Function Name : show_customer
@Description   : This function asks the user for a customer ID and
                 displays the customer details if the ID is found
                 in the database.
@Input Param   : NONE (User Input)
                 Customer ID
@Output Param  : NONE
@Author        : Prashik Dabhade
'''
def show_customer():
    c_id=input("Enter customer id:")
    cur.execute(
        "SELECT * FROM customer where id=?",
        (c_id,)
        )
    
    data=cur.fetchone()
    if data:
        print("\nCustomer Found")
        print("ID:", data[0])
        print("Name:", data[1])
        print("Mobile:", data[2])
        print("Email:", data[3])
        
    else:
        print("Customer Not Found!")
        
    
create_table()

while True:
    print("\n===== Customer Management =====")
    print("1. Add Customer")
    print("2. Search Customer")
    print("3. Update Customer")
    print("4. Show customer")
    print("5. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_customer()
        
    elif choice == "2":
        search_customer()
        
    elif choice == "3":
        update_customer()
        
    elif choice == "4":
         show_customer()

    elif choice == "5":
        print("Thank You for visiting our store!")
        break
    
    else:
        print("Invalid Choice!")
