
import matplotlib.pyplot as plt
import connection_management as cm
''' 1.function name :graph : it gives all information in form of graph
                           it automatically connect to database
                           and close it
                   input parameters : none
                   output parameters : display graph
                   
    2.function name : generate_sample_report: it gives report text of graph 
                   
                   input parameters : none
                   output parameters : generate report text file          
'''

def graph():
    try:
        connection=cm.connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(customer_id) FROM CUSTOMERS;")
        total_customers = cursor.fetchone()[0]

        # 2. Total Catalog Products Count
        cursor.execute("SELECT COUNT(product_id) FROM PRODUCTS;")
        total_products = cursor.fetchone()[0]

        # 3. Total Invoices Generated Count
        cursor.execute("SELECT COUNT(invoice_id) FROM INVOICES;")
        total_invoices = cursor.fetchone()[0]

        # 4. Total Sales Revenue Accumulation
        cursor.execute("SELECT SUM(total_amount) FROM INVOICES;")
        total_sales = cursor.fetchone()[0] or 0.0  # Fallback to 0 if no entries exist

        # 5. Low Stock Products Snapshot
        cursor.execute("""
            SELECT product_name, stock_quantity FROM PRODUCTS 
            ORDER BY stock_quantity ASC LIMIT 5; """)
        stock_results = cursor.fetchall()


        # Unpack low stock data lists
        low_stock_items = [row[0] for row in stock_results]
        stock_levels = [row[1] for row in stock_results]

        # 3. DRAW THE SNAPSHOT DASHBOARD
        fig = plt.figure(figsize=(12, 10))

        # Graph 1: Total Customers
        ax1 = plt.subplot2grid((3, 2), (0, 0))
        ax1.bar(['Total Customers'], [total_customers], color='green', edgecolor='black', width=0.4)
        ax1.set_title('1. no of customers')
        ax1.set_ylabel('Total Count')

        # Graph 2: Total Productsb
        ax2 = plt.subplot2grid((3, 2), (0, 1))
        ax2.bar(['Total products'], [total_products], color='yellow', edgecolor='black', width=0.4)
        ax2.set_title('2. no of products')
        ax2.set_ylabel('Total Count')

        # Graph 3: Total Invoices
        ax3 = plt.subplot2grid((3, 2), (1, 0))
        ax3.bar(['Total Invoices'], [total_invoices], color='blue', edgecolor='black', width=0.4)
        ax3.set_title('3. no of invoices')
        ax3.set_ylabel('Total Count')

        # Graph 4: Total Sales
        ax4 = plt.subplot2grid((3, 2), (1, 1))
        ax4.bar(['total Sales'], [total_sales], color='pink', edgecolor='black', width=0.4)
        ax4.set_title('4. Sales')
        ax4.set_ylabel('Amount')

        # Graph 5: Low stack products
        ax5 = plt.subplot2grid((3, 2), (2, 0), colspan=2)
        ax5.barh(low_stock_items, stock_levels, color='orange', edgecolor='black')
        ax5.set_title('5.Lowest Stock Items')
        ax5.set_xlabel('Current Stock Quantity')
        ax5.axvline(x=5, color='black', linestyle='--', alpha=0.5, label='stocks (<5)')
        ax5.legend()

        # Layout
        fig.suptitle('sales and products information', fontsize=16, weight='bold')
        plt.tight_layout()
        plt.show()
        connection.close()
    except:
        print("something went wrong")
        return None



def generate_simple_report():
    try:
        connection = cm.connection()
        cursor = connection.cursor()
    
        # 1. Count total rows in the customers table
        cursor.execute("SELECT COUNT(customer_id) FROM CUSTOMERS;")
        total_customers = cursor.fetchone()[0]
    
        # 2. Count total rows in the products table
        cursor.execute("SELECT COUNT(product_id) FROM PRODUCTS;")
        total_products = cursor.fetchone()[0]
    
        # 3. Count total rows in the invoices table
        cursor.execute("SELECT COUNT(invoice_id) FROM INVOICES;")
        total_invoices = cursor.fetchone()[0]
    
        # 4. Calculate total money made from all invoices
        cursor.execute("SELECT SUM(total_amount) FROM INVOICES;")
        total_sales = cursor.fetchone()[0]
    
        # If there are no sales yet, set the value to 0
        if total_sales is None:
            total_sales = 0.0
    
        cursor.execute("SELECT product_name, stock_quantity FROM PRODUCTS WHERE stock_quantity < 10;")
        low_stock_items = cursor.fetchall()
    
        with open("business_report.txt", "w") as file:
            # Write the simple text metric totals to the file
            file.write("STORE BUSINESS REPORT\n")
            file.write("=====================\n")
            file.write(f"Total Customers: {total_customers}\n")
            file.write(f"Total Products: {total_products}\n")
            file.write(f"Total Invoices: {total_invoices}\n")
            file.write(f"Total Sales Revenue: Rs {total_sales}\n\n")
    
    
            file.write("LOW STOCK PRODUCTS LIST\n")
            file.write("-----------------------\n")
    
    
            for name, qunatity in low_stock_items:
                file.write(f"Item: {name} | Stock Left: {qunatity}\n")
    
        print("Report saved successfully to business_report.txt")
        
    except:
        print("something went wrong")
        return None
    
    
