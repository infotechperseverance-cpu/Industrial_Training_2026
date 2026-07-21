
import json
import os
from Connetion_Module import connection


'''
@Function Name: gst_rates
@Description  : Loads GST rates from the JSON file if not found create new and takes defaults rates.
@inputParam   : NA
@outParam     : dictionary
@Author       : Dimpal Rajput
'''
def gst_rates():
    """Loads GST rates from the JSON  file."""
    # Default rates in case the JSON file is missing
    default_rates = {
        "Electronics": 18,
        "Grocery": 5,
        "Clothing": 12,
        "Medicines": 12,
        "Luxury": 28,
        "Stationary":18
    }
    #if json file doesnt find then new json file is created 
    if os.path.exists("gst_rates.json"):
        try:
            with open("gst_rates.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("gst_rates.json not found. Using default rates.")
            return default_rates
    else:
        
        with open("gst_rates.json", "w") as file:
            json.dump(default_rates, file, indent=4)
        return default_rates
    

'''
@Function Name: add_product
@Description  : Ask user for details Of product and stores a new item record.
@inputParam   : db_connection (an active database connection object)
@outParam     : NA
@Author       : Dimpal Rajput
'''

def add_product(db_connection):
    conn = db_connection  #links directly to the database connection 
    cursor = conn.cursor(buffered=True)

   
    gst_rules = gst_rates()
    #ask user for product name 
    print("-"*10,"Enter Product Details","-"*10)
    while True:
        product = input("Enter Product Name : ").strip()
        if product == "":
            print("Product name cannot be Empty, please try again!")
            continue

        # CHECK: Look up if this product name already exists and store product name temporarily in lowercase LOWER()
        cursor.execute("SELECT * FROM products WHERE LOWER(product_name) = %s", (product.lower(),))
        existProduct = cursor.fetchone()

        if existProduct is not None:
            #  Stop them if it exists, and loop back to ask for a new name
            print(f"A product named '{product}' already exists in your inventory!")
            print("Please enter a unique product name.\n")
            continue
        break

# converts  all category to lowecase and stored in rules {}
    rules= {key.lower(): key for key in gst_rules}
    while True:        
        category = input("Category of product : ").strip()
        
        if category.lower() in rules:
            CategoryData = rules[category.lower()]
            gst_percent = gst_rules[CategoryData]
        
            print(f"✅ Category Recognized: '{CategoryData}'! GST rate: {gst_percent}%")
            break
        else:
            print(f"'{category}' is not a valid category ")
            print(f"Available choices are: {', '.join(gst_rules.keys())}")
            print("Please try again.\n")


#Ask user for stock of product
    while True:
        try:
            stock=int(input("Enter Stock of Product : "))
            if stock > 0:
                break
            else:
                print("Enter a Valid stock Quantity")
        except ValueError:
            print("ERROR : Stock must be an Integer")
# ask user for product price
    while True:   
        try:
            price=float(input("Enter Price : "))
            if price > 0:
                break
            else:
                print("Enter a Valid price ")
        except ValueError:
            print("ERROR : Price must be a Number ")

    cursor.execute('''
        INSERT INTO products (product_name, category, price, gst_percent, stock_quantity)
        VALUES (%s, %s, %s, %s, %s)
    ''', (product, CategoryData, price, gst_percent, stock))
    product_id=cursor.lastrowid

    # 4. SAVE AND CLOSE 
    conn.commit()  # This saves the new product to file
    print(f"✅ Product Added Successfully!")
    print(f"Generated Product ID : {product_id}")
    cursor.close()   # Closes the cursor safely
    


#=====================================================================================================
'''
@Function Name: update_product
@Description  : updates the product records ask user for update stock,delete product, update price
                by refering the productid we can update 
@inputParam   : db_connection (an active database connection object)
@outParam     : NONE
@Author       : Dimpal Rajput
'''
def update_product(db_connection):
    conn = db_connection  #Passed database connection  into the parameter
    cursor = conn.cursor()
    print("-"*10,"Update product Details","-"*10)
    #ask user for productId and search in table  and fetches that single row
    while True:
        try:
            productId = int(input("Enter Product ID: "))

            cursor.execute(
                "SELECT * FROM products WHERE product_id = %s",
                (productId,)
            )

            product_data = cursor.fetchone()

            if product_data:
                break
            else:
                print("Product ID not found. Please enter a valid Product ID.")

        except ValueError:
            print("Product ID must be a number.")


    #display menu to user for update what they has to update
    print(f"Product id found {product_data[1]} Current Stock : {product_data[5]} current price : {product_data[3]}")
    print("What Would you like to update : ")
    print("1.Update Stock ")
    print("2.Update Price")
    print("3.Delete record")
    print("4.Back")
 
  
    ch=input("Enter option 1-4: ").strip()

    #asks for new stock
    if ch=="1":
        while True:
            try:
                nStock=int(input("Enter new Stock : "))
                if nStock >=0:
                    cursor.execute("UPDATE products SET stock_quantity=%s WHERE product_id=%s",(nStock,productId))
                    break
                else:
                    print("ERROR: Stock cannot be Negative ")
            except ValueError:
                print("ERROR : Stock must be an Integer")
        
        print("✅product Stock updated Successfully !")

    #asks for new price
    elif ch=="2":
        while True:
       
            try:
                nPrice=float(input("Enter New Price of a Product : "))
                if nPrice >0:
                    cursor.execute("UPDATE products SET price=%s WHERE product_id=%s",(nPrice,productId))
                    break
                else:
                    print("Please Enter Valid Price ")
            except ValueError:
                print("ERROR : Price must be a Number ")
        print("✅product Price updated Successfully !")

    # asks user to delete the entire product
    elif ch=='3':
        while True:
           
            delete=input(f"Are you sure to delete product {product_data[1]} permanently ? ").lower().strip()
            if delete =="yes" or delete=='y':
                cursor.execute("DELETE FROM products WHERE product_id=%s",(productId,))   
                print(f"Product {product_data[1]} has been deleted successfully !")
                break
            elif delete=="no" or delete=='n':
                print("Deletion cancelled ! Your product is safe")
                break
            else:
                print("Type Yes or No")
            break
    #back to main menu
    elif ch=="4":
        print("Moving back to main menu ")
        # id user enters invalid choice
    else:
        print("Invalid Input")
    
    conn.commit()
    cursor.close()


'''
@Function Name: display_products
@Description  :fetches all records from table retrieves data from the table and 
               display on terminal 
@inputParam   : db_connection (an active database connection object)
@outParam     : NONE
@Author       : Dimpal Rajput
'''
def display_products(db_connection):
    print("-"*38,"Available Product List","-"*38)
    conn = db_connection  # FIXED: Standardized connection strategy
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    records=cursor.fetchall()

    cursor.close()
    if(len(records)==0):
        print("NO Product Found in the database, first add products ")
    else:
        print(f"{'product_id':<15} {'product_name':<15} {'category':<15} {'price':<10} {'gst_percent %':<14} {'stock_quantity':<15} ")
        for row in records:
            print(f"{row[0]:<15} {row[1]:<15} {row[2]:<15} Rs.{row[3]:<8.2f} {row[4]:<14} {row[5]:<15} ")
    print("-" * 100)


def product_menu(db_connection):

    while True:

        print("\n========== PRODUCT MANAGEMENT ==========")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Display Products")
        print("4. Back")

        choice = input("Enter Choice : ")

        if choice == "1":
            add_product(db_connection)

        elif choice == "2":
            update_product(db_connection)

        elif choice == "3":
            display_products(db_connection)

        elif choice == "4":
            break

        else:
            print("Invalid Choice. Please Try Again.")
<<<<<<< HEAD
=======



>>>>>>> 1295afc (Final code)
