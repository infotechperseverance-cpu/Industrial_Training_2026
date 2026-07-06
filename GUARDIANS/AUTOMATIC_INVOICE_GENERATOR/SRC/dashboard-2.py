import json
import os
from collections import defaultdict

INVOICE_FILE = "invoices.json"
class SalesDashboard:

    def __init__(self):
        self.f_name = INVOICE_FILE
        self.inv_list = self.load_invoices()

    # Reading invoice data 
    def load_invoices(self):

        if not os.path.exists(self.f_name):
            return []

        try:
            with open(self.f_name, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def total_sales(self):

        tot = 0

        for invoice_id, inv in self.inv_list.items():
            tot += inv["total_price"]

        return tot
    
    def total_invoices(self):
        return len(self.inv_list)

    # showing top selling product
    def top_selling_products(self):

        if len(self.inv_list) == 0:
            print("\nNo sales data available.")
            return

        prod_sales = defaultdict(int)

        for invoice_id, inv in self.inv_list.items():

            for item in inv["items"]:
                prod_sales[item["name"]] += item["quantity"]

        print("\n-------- Top Selling Products ------")

        sort_p = sorted(
            prod_sales.items(),
            key=lambda p: p[1],
            reverse=True
        )

        for name, qty in sort_p:
            print(f"{name} : {qty} Sold")
# Display  sales
    def monthly_sales(self):

        print("\n========== Monthly Sales ==========")

        total = self.total_sales()

        print(f"Current Sales : ₹{total:.2f}")

    def show_dashboard(self):
        print("\n")
        print("=" * 45)
        print("         SALES DASHBOARD")
        print("=" * 45)

        print(f"Total Sales     : ₹{self.total_sales():.2f}")
        print(f"Total Invoices  : {self.total_invoices()}")

        self.top_selling_products()
        self.monthly_sales()

        print("=" * 45)

                 