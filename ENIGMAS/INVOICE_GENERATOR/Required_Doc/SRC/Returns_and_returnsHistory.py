
from datetime import date
from Connetion_Module import connection
from search_invoice import search_invoice
"""
@function name: return_product
@description: this product make product return process possible 
@input:none
@output:none
@author:
"""
def return_product(invoice_id=None):
    conn = None
    try:
        
        conn = connection()
        cursor = conn.cursor()
        if invoice_id is None:
            invoice_id = int(input("Enter Invoice ID : "))
        product_id = int(input("Enter Product ID : "))
        quantity = int(input("Enter Return Quantity : "))
        reason = input("Enter Return Reason : ")

        # Check Invoice
        cursor.execute("SELECT invoice_date FROM invoices WHERE invoice_id=%s",(invoice_id,) )

        invoice = cursor.fetchone()

        if invoice is None:
            print("Invoice Not Found")
            return

        invoice_date = invoice[0]

        # Get Product Category
        cursor.execute("SELECT category FROM products WHERE product_id=%s",(product_id,))

        product = cursor.fetchone()

        if product is None:
            print("Product Not Found")
            return

        category = product[0]

        days = (date.today() - invoice_date).days

        if category.lower() == "grocery":
            if days > 3:
                print("Grocery Return Period Expired")
                return
        else:
            if days > 7:
                print("Return Period Expired")
                return

        # Check Purchased Quantity
        cursor.execute("""
            SELECT quantity FROM invoice_items WHERE invoice_id=%s AND product_id=%s
            """,(invoice_id, product_id))

        item = cursor.fetchone()

        if item is None:
            print("Product Not Purchased")
            return

        if quantity <= 0:
            print("Return quantity must be greater than 0")
            return

        if quantity > item[0]:
            print("Invalid Return Quantity")
            return
        # Save Return
        cursor.execute("""INSERT INTO returns
            (invoice_id,product_id,quantity,return_date,return_reason)
            VALUES(%s,%s,%s,%s,%s)""",(invoice_id, product_id, quantity, date.today(), reason))

        # Update Stock
        cursor.execute(""" UPDATE products SET stock_quantity=stock_quantity+%s
            WHERE product_id=%s""",(quantity, product_id))

        conn.commit()
        print("Return Successful")

        cursor.close()
        conn.close()

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error :", e)

"""
@function name: return_history  
@description: show all return history of product
@input:none
@output:none
@author:
"""
def return_history():
    conn = None
    cursor = None

    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("""SELECT r.return_id,r.invoice_id,p.product_name,r.quantity,r.return_date,
        r.return_reason FROM returns r JOIN products p ON r.product_id=p.product_id""")

        records = cursor.fetchall()

        if len(records) == 0:
            print("No Return History")
            return

        print("\nReturn History")
        print("-" * 70)

        for row in records:
            print("Return ID   :", row[0])
            print("Invoice ID  :", row[1])
            print("Product     :", row[2])
            print("Quantity    :", row[3])
            print("Date        :", row[4])
            print("Reason      :", row[5])
            print("-" * 70)

    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()
"""
function name: returns
@description: show choice selection of module
@input:none
@output:none
@author:
"""

def returns(invoice_id=None):
    while True:

        print("\n===== RETURN MODULE =====")
        print("1. Return Product")
        print("2. Return History")
        print("3. Exit")

        choice = input("Enter Choice : ")

        if choice == "1":

            if invoice_id is None:
                invoice_id = search_invoice()

            if invoice_id:
                return_product(invoice_id)

        elif choice == "2":
            return_history()

        elif choice == "3":
            print("Thank You")
            return

        else:
            print("Invalid Choice")