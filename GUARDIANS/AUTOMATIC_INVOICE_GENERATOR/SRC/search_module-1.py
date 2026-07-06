import json
import os

CUSTOMER_FILE = "customers.json"
PRODUCT_FILE = "products.json"
INVOICE_FILE = "invoices.json"

class SearchModule:
    def __init__(self):
        pass

                # Read data
    def load_data(self, f_name):
        if not os.path.exists(f_name):
            return []
        try:
            with open(f_name, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            return []

    # Search invoice 
    def search_invoice(self):
        inv_list = self.load_data(INVOICE_FILE)

        # Removed the instant exit check from here so user can type input first

        kw = input("\nEnter Invoice ID, Customer ID or Name : ").strip().lower()
        if kw == "":
            print("Search field cannot be empty.")
            return

        if len(inv_list) == 0:
            print("No invoice records found .")
            return

        found = False

        for invoice_id, inv in inv_list.items():

            inv_id = invoice_id.strip().lower()
            cust_id = str(inv.get("customer_id", "")).strip().lower()
            cust_nm = str(inv.get("customer_name", "")).strip().lower()

            if kw == inv_id or kw == cust_id or kw in cust_nm:

                print("\n//////// Invoice Details ////////")
                print(f"Invoice ID  : {invoice_id}")
                print(f"Customer ID : {inv['customer_id']}")
                print(f"Customer    : {inv['customer_name']}")
                print(f"Subtotal    : ₹{inv['subtotal']}")
                print(f"GST         : ₹{inv['GST']}")
                print(f"Discount    : ₹{inv['discount']}")
                print(f"Total Amount: ₹{inv['total_price']}")

                print("\nPurchased Products")

                for item in inv["items"]:
                    print(f"- {item['name']} ({item['quantity']}) = ₹{item['total']}")

                found = True
                break

        if not found:
            print("Invoice not found.")
