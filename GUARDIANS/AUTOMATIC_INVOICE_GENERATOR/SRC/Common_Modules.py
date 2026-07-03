import os
import json
import re

def read_file(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as file:
            return json.load(file)
    else:
        return []

def write_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
        file.close()

def customer_input():
    while True:
        customer_id = input("enter customer id: ")
        if customer_id.isdigit():
            customer_id = int(customer_id)
            x = read_file("customer.json")
            for customer in x:
                if customer["customer_id"] == customer_id:
                    print("customer id already exists")
                    return False
            else:
                customer_id = int(customer_id)
                return customer_id
        else:
            print("enter a valid customer ID")

def name_input():
    while True:
        name = input("Enter name: ")
        if all(part.isalpha() for part in name.split()):
            return name
        else:
            print("invalid name! try again ")

def email_input():
    while True:
        email = input("enter email: ")
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if re.match(pattern, email):
            return email

        else:
            print("invalid email! try again")

def phone_input():
    while True:
        phone = input("enter phone number: ")
        phone = phone.replace(" ", "")
        if phone.isdigit() and len(phone) == 10:
            return phone
        else:
            print("invalid phone number! try again")

def city_input():
    while True:
        city = input("Enter city: ")
        if all(part.isalpha() for part in city.split()):
            return city
        else:
            print("Invalid city! Try again")

