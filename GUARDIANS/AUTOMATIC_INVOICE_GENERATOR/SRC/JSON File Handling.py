import os
import json
from common_modules import *


class Handling:
    def __init__(self, name="", email="", city="", phone="", customer_id=0):
        self.name = name
        self.email = email
        self.city = city
        self.phone = phone
        self.customer_id = customer_id

    def add_customer_info(self):
        data = read_file("customers.json")   
        record = {
            "name": self.name,
            "customer_id": self.customer_id,
            "email": self.email,
            "city": self.city,
            "phone": self.phone
        }

        data[str(self.customer_id)] = record    
        write_file("customers.json", data)
        print("Customer added successfully!")
    
    def update_customer_info(self, customer_id):
        data = read_file("customers.json")

        if not data:
            print("Customer list is empty!")
            return

        customer = data.get(str(customer_id))

        if customer:
            customer["name"] = name_input()
            customer["email"] = email_input()
            customer["city"] = city_input()
            customer["phone"] = phone_input()

            write_file("customers.json", data)
            print("Customer updated successfully!")
        else:
            print("Customer not found")

    def remove_customer_info(self, customer_id):
        data = read_file("customers.json")

        if not data:
            print("Customer list is empty")
            return

        if str(customer_id) in data:
            del data[str(customer_id)]
            write_file("customers.json", data)
            print("Customer removed successfully!")
        else:
            print("Customer not found")

    def show_customers_info(self):
        if os.path.exists("customers.json") and os.path.getsize("customers.json") > 0:
            data = read_file("customers.json")
            if not data:
                print("Customer list is empty ")
                return
            for customer in data.values():
                print("__________________________________")
                print("Customer ID :", customer["customer_id"])
                print("Name        :", customer["name"])
                print("Email       :", customer["email"])
                print("City        :", customer["city"])
                print("Phone No.   :", customer["phone"])
        else:
            print("file does not exist")