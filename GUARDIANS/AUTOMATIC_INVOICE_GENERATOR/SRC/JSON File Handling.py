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
        data = read_file("customer.json")

        record = {
            "name": self.name,
            "customer_id": self.customer_id,
            "email": self.email,
            "city": self.city,
            "phone": self.phone
        }
        data.append(record)
        write_file("customer.json", data)

        if not os.path.exists("customer.json"):
            record = {
                "name": self.name,
                "customer_id": self.customer_id,
                "email": self.email,
                "city": self.city,
                "phone": self.phone
            }
            data.append(record)
            write_file("customer.json", data)

    def update_customer_info(self, customer_id):
        self.customer_id = customer_id
        data = read_file("customer.json")
        if os.path.exists("customer.json") and os.path.getsize("customer.json") > 0:
            for customer in data:
                if customer["customer_id"] == self.customer_id:
                    while True:
                        customer["customer_id"] =  input("enter customer id: ")
                        if customer["customer_id"].isdigit():
                            customer["customer_id"] = int(customer_id)
                            break
                        else:
                            print("customer id is not valid")

                    customer["name"] = name_input()
                    customer["email"] = email_input()
                    customer["city"] = city_input()
                    customer["phone"] = phone_input()

                    with open("customer.json", "w") as file:
                        json.dump(data, file, indent=4)
                    print("Customer updated successfully!")
                    break

            else:
                print("Customer not found!")

        else:
            print("Customer list is empty !")

    def remove_customer_info(self, customer_id):
        data = read_file("customer.json")

        if not data:
            print("Customer list is empty !")

        else:
            for i in range(len(data)):
                if data[i]["customer_id"] == customer_id:
                    del data[i]
                    write_file("customer.json", data)
                    print("Customer removed successfully!")
                    break
            else :
                print("Customer not found!")

    def show_customers_info(self):
        if os.path.exists("customer.json") and os.path.getsize("customer.json") > 0:
            data = read_file("customer.json")
            if not data:
                print("Customer list is empty !")
            else:
                for i in data:
                    print("__________________________________")
                    print("customer_id  : ",i["customer_id"])
                    print("name         : ",i["name"])
                    print("email        : ",i["email"])
                    print("city         : ",i["city"])
                    print("phone no.    : ",i["phone"])
        else:
            print("file does not exist!")