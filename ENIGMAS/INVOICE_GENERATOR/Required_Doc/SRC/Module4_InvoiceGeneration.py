import mysql.connector
from datetime import datetime 

'''
@Function Name: invoice_generation
@Description  : This function accepts an active MySQL database connection, handles live user 
                inputs for cashier/customer validation, processes product shopping cart 
                selections, calculates bill subtotals, applies discounts, calculates GST, 
                updates inventory stock, and saves transaction records to invoices and invoice_items tables.
@inputParam   : db_connection (an active MySQL database connection object)
@outParam     : NONE
@Author       : Dimpal Rajput
'''
def invoice_generation(db_connection):
    print("-" * 15 + "GENERATING INVOICE" + "-" * 15)
    cursor = db_connection.cursor()
    
    final_subtotal = 0.0
    final_gst = 0.0
    
    # 1. Cashier Validation 
    while True:
        
        username = input("Enter User Name: ").strip()

        cursor.execute(
            "SELECT user_id, username FROM users WHERE LOWER(username) = LOWER(%s)",
            (username,)
        )

        userData = cursor.fetchone()

        if userData:
            userId = userData[0]        # user_id
            username = userData[1]      # username

            print(f"Cashier : {username}")
            break
        else:
            print("Invalid Username")

        

    # 2. User Validation
    while True:
        try:
            customerId = int(input("Enter Customer Id : "))
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customerId,))
            customerData = cursor.fetchone()
            if customerData:
                print(f"Customer is found {customerData[1]}")
                break
            elif not customerData:
                print(f"Customer Id not found ,please try again")
        except ValueError:
            print("ERROR : Customer Id must be a Number ")

    invoice_list = [] #add invoice list of products

    # 3. Product Selection Loop
    # ask user for productID
    while True:
        try:
            productId = int(input("Enter Product Id (or 0 to complete bill): "))
            if productId == 0:
                if not invoice_list:
                    print("Cart is Empty cannot generate invoice ")
                    continue
                break

            cursor.execute("SELECT * FROM products WHERE product_id = %s", (productId,))
            productData = cursor.fetchone()

            if not productData:
                print("There is no product please first add the product")
                continue
            
            print(f"product Found product Name: {productData[1]} Price {productData[3]} Stock: {productData[5]}")
            
            #check if stocks are greater than or equals to 0
            if productData[5] <= 0:
                print("Out of Stock! Cannot add this product ")
                continue

            #asks for Quantity
            while True:
                try:
                    quantity = int(input(f"Enter Quantity {productData[1]}: "))
                    if quantity <= 0:# checks if greater or eqaul to 0
                        print("Quantity must be greater than zero ")
                        continue

                    if quantity <= int(productData[5]):
                        # 1. Convert all database items into standard numbers first
                        unit_price = float(productData[3])
                        gst_percent = float(productData[4])
                        current_stock = int(productData[5])

                        # 2. Perform the calculations 
                        itemSTotal = unit_price * quantity
                        item_gst = itemSTotal * (gst_percent / 100.0)
                        item_total = itemSTotal + item_gst

                        # 3. Save everything to your cart list
                        invoice_list.append({
                            'product_id': productId,
                            'quantity': quantity,
                            'unit_price': unit_price,
                            'subtotal': itemSTotal,
                            'gst': item_gst,
                            'total': item_total,
                            'new_stock': current_stock - quantity
                        })

                        # 4. Update the running counter totals
                        final_subtotal += itemSTotal
                        final_gst += item_gst
                        print(f"Added to cart {productData[1]} * {quantity}")
                        break
                    else:
                        print(f"Insufficient stock only {productData[5]} items available")
                except ValueError:
                    print("quantity must be a number")
        except ValueError:
            print("product Id Must be a number ")

    # 4. Final Bill Calculations & Database Storage Execution
    try:
        currentDate = datetime.now().strftime(r"%Y-%m-%d")
        try:
            inputDiscount = float(input("Enter discount or 0 : "))
        except ValueError:
            inputDiscount = 0.0

        final_total = (final_subtotal - inputDiscount) + final_gst

        # Insert data into invoices table
        cursor.execute("""
            INSERT INTO invoices (customer_id, user_id, invoice_date, subtotal, gst_amount, discount, total_amount, pdf_path, email_status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (customerId, userId, currentDate, final_subtotal, final_gst, inputDiscount, final_total, "", "Pending"))
        
        invoice_id = cursor.lastrowid

        # Insert item loops into individual rows inside invoice_items table
        for item in invoice_list:
            cursor.execute("""
                INSERT INTO invoice_items (invoice_id, product_id, quantity, unit_price, gst_amount, total_price) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (invoice_id, item['product_id'], item['quantity'], item['unit_price'], item['gst'], item['total']))
            
            # Deduct quantities directly out of the main product stock
            cursor.execute("""
                UPDATE products 
                SET stock_quantity = %s 
                WHERE product_id = %s
            """, (item['new_stock'], item['product_id']))
            
        # FIXED: Moved outside of the 'for' loop to commit the whole cart transaction cleanly at once
        db_connection.commit()
        print(f"\nTransaction saved successfully! Generated Invoice ID: {invoice_id}")

    except mysql.connector.Error as e:
        db_connection.rollback()
        print(f"Database error encountered: Transaction rolled back. -> {e}")
        
    finally:
        cursor.close()

