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

s = Handling()
a = Input()
t = True
while t:
    print("_________________________________")
    c = int(input("enter choise : \n1. add customer\n2. update customer\n3. remove customer\n4. show all customers info\n5. exit\n choise : "))

    if c == 1:
        a.add_customer()
    elif c == 2:
        a.update_customer()
    elif c == 3:
        a.remove_customer()
    elif c == 4:
        s.show_customers_info()
    elif c == 5:
        t = False
    else:
        print("invalid choice")







