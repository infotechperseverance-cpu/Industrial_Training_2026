import json

# Customer Module
from Invoice_1 import Input
from module10 import Handling

# Product Module
from product_module import ProductManager

# Invoice Module
from invoice_generation import Automatic_invoice_generator

# Search Module
from search_module import SearchModule

# Dashboard Module
from dashboard import SalesDashboard

# PDF Module
from pdf_generation import InvoiceManager as PDFManager

# Email Module
from email_sender import InvoiceManager as EmailManager

# Reset Module
from reset import InvoiceManager as ResetManager


class MainMenu:

    def __init__(self):

        self.customer = Input()
        self.customer_show = Handling()

        self.product = ProductManager()

        self.invoice = Automatic_invoice_generator()

        self.search = SearchModule()

        self.dashboard = SalesDashboard()

        self.pdf = PDFManager("invoices.json")

        self.email = EmailManager("customers.json")

        self.reset = ResetManager()

    # CUSTOMER MENU 

    def customer_menu(self):

        while True:

            print("\n")
            print("=" * 45)
            print("         CUSTOMER MANAGEMENT")
            print("=" * 45)
            print("1. Add Customer")
            print("2. Update Customer")
            print("3. Remove Customer")
            print("4. Show Customers")
            print("5. Back")
            print("=" * 45)

            choice = input("Enter your choice : ")

            if choice == "1":
                self.customer.add_customer()

            elif choice == "2":
                self.customer.update_customer()

            elif choice == "3":
                self.customer.remove_customer()

            elif choice == "4":
                self.customer_show.show_customers_info()

            elif choice == "5":
                break

            else:
                print("Invalid Choice")

    # PRODUCT MENU

    def product_menu(self):

        while True:

            print("\n")
            print("=" * 45)
            print("          PRODUCT MANAGEMENT")
            print("=" * 45)
            print("1. Add Product")
            print("2. Update Product")
            print("3. Remove Product")
            print("4. Back")
            print("=" * 45)

            choice = input("Enter your choice : ")

            if choice == "1":
                self.product.add_product()

            elif choice == "2":
                self.product.update_product()

            elif choice == "3":
                self.product.remove_product()

            elif choice == "4":
                break

            else:
                print("Invalid Choice")

   # INVOICE MENU 

    def invoice_menu(self):

        while True:

            print("\n")
            print("=" * 45)
            print("          INVOICE MANAGEMENT")
            print("=" * 45)
            print("1. Generate Invoice")
            print("2. Back")
            print("=" * 45)

            choice = input("Enter your choice : ")

            if choice == "1":

                customer_id = input("Enter Customer ID : ")
                customer_name = input("Enter Customer Name : ")

                self.invoice.invoice_generation(
                    customer_id,
                    customer_name
                )

            elif choice == "2":
                break

            else:
                print("Invalid Choice")

    # SEARCH MENU

    def search_menu(self):

        while True:

            print("\n")
            print("=" * 45)
            print("            SEARCH MENU")
            print("=" * 45)
            print("1. Search Invoice")
            print("2. Back")
            print("=" * 45)

            choice = input("Enter your choice : ")

            if choice == "1":
                self.search.search_invoice()

            elif choice == "2":
                break

            else:
                print("Invalid Choice")

    # PDF GENERATION MENU
    def pdf_menu(self):

        while True:

            print("\n")
            print("=" * 45)
            print("         PDF GENERATION")
            print("=" * 45)
            print("1. Generate Invoice PDF")
            print("2. Back")
            print("=" * 45)

            choice = input("Enter your choice : ")

            if choice == "1":

                invoice_id = input("Enter Invoice ID : ")

                self.pdf.pdf_generation(invoice_id)

            elif choice == "2":
                break

            else:
                print("Invalid Choice")

    # DASHBOARD MENU

    def dashboard_menu(self):

        while True:

            print("\n")
            print("=" * 45)
            print("          SALES DASHBOARD")
            print("=" * 45)
            print("1. View Dashboard")
            print("2. Refresh Dashboard")
            print("3. Back")
            print("=" * 45)

            choice = input("Enter your choice : ")

            if choice == "1":

                self.dashboard.show_dashboard()

            elif choice == "2":

                self.dashboard.inv_list = self.dashboard.load_invoices()
                print("Dashboard Refreshed Successfully")

            elif choice == "3":

                break

            else:

                print("Invalid Choice")

    # EMAIL MENU

    def email_menu(self):

        while True:

            print("\n")
            print("=" * 45)
            print("          EMAIL MODULE")
            print("=" * 45)
            print("1. Send Invoice Email")
            print("2. Back")
            print("=" * 45)

            choice = input("Enter your choice : ")

            if choice == "1":

                invoice_id = input("Enter Invoice ID : ")

                try:

                    with open("invoices.json", "r") as file:
                        invoices = json.load(file)

                    if invoice_id in invoices:

                        customer_id = invoices[invoice_id]["customer_id"]

                        sender = input("Enter Sender Email : ")
                        password = input("Enter App Password : ")

                        self.email.email_sending(
                            sender,
                            password,
                            customer_id,
                            f"{invoice_id}.pdf"
                        )

                    else:

                        print("Invoice Not Found")

                except Exception as e:

                    print("Error :", e)

            elif choice == "2":

                break

            else:

                print("Invalid Choice")

    # RESET MENU

    def reset_menu(self):

        while True:

            print("\n")
            print("=" * 45)
            print("           RESET MENU")
            print("=" * 45)
            print("1. Reset All Data")
            print("2. Back")
            print("=" * 45)

            choice = input("Enter your choice : ")

            if choice == "1":

                self.reset.reset_data()

            elif choice == "2":

                break

            else:

                print("Invalid Choice")
        # ================= MAIN MENU =================

    def main_menu(self):

        while True:

            print("\n")
            print("=" * 55)
            print("         INVOICE MANAGEMENT SYSTEM")
            print("=" * 55)
            print("1. Customer Management")
            print("2. Product Management")
            print("3. Invoice Management")
            print("4. Search")
            print("5. Sales Dashboard")
            print("6. Generate PDF")
            print("7. Send Email")
            print("8. Reset Data")
            print("9. Exit")
            print("=" * 55)

            choice = input("Enter your choice : ")

            if choice == "1":

                self.customer_menu()

            elif choice == "2":

                self.product_menu()

            elif choice == "3":

                self.invoice_menu()

            elif choice == "4":

                self.search_menu()

            elif choice == "5":

                self.dashboard_menu()

            elif choice == "6":

                self.pdf_menu()

            elif choice == "7":

                self.email_menu()

            elif choice == "8":

                self.reset_menu()

            elif choice == "9":

                print("\nThank You for Using Invoice Management System")
                print("Exiting Program...")
                break

            else:

                print("Invalid Choice! Please Try Again.")


# ================= START PROGRAM =================

if __name__ == "__main__":

    obj = MainMenu()

    obj.main_menu()                                   