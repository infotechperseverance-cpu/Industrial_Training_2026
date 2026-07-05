import os
import json
from module10 import *
from common_modules import *

class Input :
    def __init__(self):
        pass

    def add_customer(self):
        customer_id = customer_input()
        if customer_id != False:
            name = name_input()
            email = email_input()
            phone = phone_input()
            city = city_input()

            x = Handling(name,email,city,phone,customer_id)
            x.add_customer_info()

    def update_customer(self):
        x = Handling()
        if os.path.exists("customer.json"):
            while True:
                n = input("enter customer id to change information: ")
                if n.isdigit():
                    n = int(n)
                    x.update_customer_info(n)
                    break
                else:
                    print("Invalid Customer Number")
        else:
            print("file does not exist")

    def remove_customer(self):
        x = Handling()
        if os.path.exists("customer.json"):
            while True:
                n = input("enter customer id to delete information: ")
                if n.isdigit():
                    n = int(n)
                    x.remove_customer_info(n)
                    break
                else:
                    print("Invalid Customer Number")
        else:
            print("file does not exist")



