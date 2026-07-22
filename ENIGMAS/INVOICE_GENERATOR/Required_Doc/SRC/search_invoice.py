from Connetion_Module import connection
import pytesseract
import re
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


'''
@Function Name : search_invoice_by_id
@Description   : Searches an invoice using the Invoice ID and
                 displays the invoice details if found.
@Input Param   : invoice_id (INT)
@Output Param  : Returns invoice_id if found, otherwise None
@Author        : Your Team
'''
def search_invoice_by_id(invoice_id):

    conn = None
    cursor = None

    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT invoice_id,
                   customer_id,
                   user_id,
                   invoice_date,
                   subtotal,
                   gst_amount,
                   discount,
                   total_amount
            FROM invoices
            WHERE invoice_id=%s
        """, (invoice_id,))

        invoice = cursor.fetchone()

        if invoice:

            print("\n========== INVOICE FOUND ==========")
            print("Invoice ID :", invoice[0])
            print("Customer ID:", invoice[1])
            print("User ID    :", invoice[2])
            print("Date       :", invoice[3])
            print("Subtotal   :", invoice[4])
            print("GST Amount :", invoice[5])
            print("Discount   :", invoice[6])
            print("Total Bill :", invoice[7])
            cursor.execute("""
            SELECT
            products.product_id,
            products.product_name,
            invoice_items.quantity
            FROM invoice_items
            JOIN products
            ON invoice_items.product_id = products.product_id
            WHERE invoice_items.invoice_id=%s
            """,(invoice_id,))

            items = cursor.fetchall()

            print("\nPurchased Products")
            print("----------------------------")

            for item in items:
                print(
                    f"Product ID : {item[0]} | "
                    f"Name : {item[1]} | "
                    f"Qty : {item[2]}"
                )

            return invoice[0]

        else:
            print("Invoice Not Found.")
            return None

    except Exception as e:
        print("Error :", e)
        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


'''
@Function Name : manual_search
@Description   : Takes Invoice ID from the user and searches it.
@Input Param   : None
@Output Param  : Returns invoice_id if found
'''
def manual_search():

    while True:

        try:
            invoice_id = int(input("Enter Invoice ID : "))
            return search_invoice_by_id(invoice_id)

        except ValueError:
            print("Invoice ID must be a number.")


def search_by_image():

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = askopenfilename(
        title="Select Invoice Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    root.destroy()

    if file_path == "":
        print("No image selected.")
        return None

    try:
        image = Image.open(file_path)

        text = pytesseract.image_to_string(image)

        print("\nReading Invoice Image...")

        print(text)

        match = re.search(
            r"Invoice\s*ID\s*[:#]?\s*(\d+)",
            text,
            re.IGNORECASE
        )

        if not match:
            print("Invoice ID not found.")
            return None

        invoice_id = int(match.group(1))

        print("Detected Invoice ID :", invoice_id)

        return search_invoice_by_id(invoice_id)

        
    except Exception as e:
        print("OCR Error :", e)
        return None
    

'''
@Function Name : search_invoice
@Description   : Displays the Invoice Search menu.
@Input Param   : None
@Output Param  : Returns invoice_id if found, otherwise None
'''
def search_invoice():

    while True:

        print("\n===== SEARCH INVOICE =====")
        print("1. Search by Invoice ID")
        print("2. Search by Image")
        print("3. Back")

        choice = input("Enter Choice : ")

        if choice == "1":
            invoice_id = manual_search()

            if invoice_id:
                return invoice_id

        elif choice == "2":
            invoice_id = search_by_image()

            if invoice_id:
                return invoice_id

        elif choice == "3":
            return None

        else:
            print("Invalid Choice.")