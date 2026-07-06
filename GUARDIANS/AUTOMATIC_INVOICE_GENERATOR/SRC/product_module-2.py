import json
import os

PRODUCT_FILE = "products.json"

class ProductManager:
    def __init__(self):
        self.f_name = PRODUCT_FILE
        self.products = self.load_data()

                    # Read product
    def load_data(self):
        if not os.path.exists(self.f_name):
            return {}
        try:
            with open(self.f_name, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
   
    def save_data(self):
        with open(self.f_name, "w") as file:
            json.dump(self.products, file, indent=4)
     
    def chk_id(self, pid):
       return pid in self.products

 # Add produt
    def add_product(self):
        print("\n========== Add Product ==========")

        pid = input("Enter Product ID : ").strip()

        if pid == "":
            print("Product ID cannot be empty.")
            return

        if self.chk_id(pid):
            print("Product ID already exists.")
            return

        nm = input("Enter Product Name : ").strip()

        if nm == "":
            print("Product name cannot be empty.")
            return
        cat = input("Enter Category : ").strip()

        if cat == "":
            print("Category cannot be empty.")
            return

        try:
            pr = float(input("Enter Price : "))

            if pr <= 0:
                print("Price must be greater than zero.")
                return

        except ValueError:
            print("Invalid price.")
            return

        try:
            st = int(input("Enter Stock Quantity : "))

            if st < 0:
                print("Stock cannot be negative.")
                return

        except ValueError:
            print("Invalid stock quantity.")
            return

        new_item = {
            "id": pid,
            "name": nm,
            "category": cat,
            "price": pr,
            "stock": st
        }

        self.products[pid] = new_item
        self.save_data()

        print("\nProduct added successfully.")

# Update product details
    def update_product(self):

        if len(self.products) == 0:
            print("\nNo products available.")
            return

        pid = input("\nEnter Product ID : ").strip()

        if pid not in self.products:
            print("Product ID not found.")
            return

        p = self.products[pid]

        print("\nLeave field blank if you don't want to change it.")

        new_nm = input(f"Name ({p['name']}) : ").strip()
        new_cat = input(f"Category ({p['category']}) : ").strip()
        new_pr = input(f"Price ({p['price']}) : ").strip()
        new_st = input(f"Stock ({p['stock']}) : ").strip()

        if new_nm:
            p["name"] = new_nm

        if new_cat:
            p["category"] = new_cat

        if new_pr:
            try:
                val = float(new_pr)
                if val <= 0:
                    print("Invalid price.")
                    return
                p["price"] = val
            except ValueError:
                print("Invalid price.")
                return

        if new_st:
            try:
                val = int(new_st)
                if val < 0:
                    print("Invalid stock.")
                    return
                p["stock"] = val
            except ValueError:
                print("Invalid stock.")
                return

        self.save_data()
        print("\nProduct updated successfully.")
    def remove_product(self):

        if len(self.products) == 0:
            print("\nNo products available.")
            return

        pid = input("\nEnter Product ID : ").strip()

        if pid not in self.products:
            print("Product ID not found.")
            return

        conf = input("Delete this product? (Y/N) : ").strip().lower()

        if conf == "y":
            del self.products[pid]
            self.save_data()
            print("Product deleted successfully.")
        else:
            print("Delete cancelled.")