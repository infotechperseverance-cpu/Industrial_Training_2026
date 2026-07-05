import os
import json

INVOICE_FILE = "invoices.json"
PRODUCT_FILE = "products.json"


# Load invoices
def load_invoices():

    if os.path.exists(INVOICE_FILE):

        with open(INVOICE_FILE, "r") as file:

            try:
                return json.load(file)

            except json.JSONDecodeError:
                return {}

    return {}


# Write invoices
def write_invoices(invoices):

    with open(INVOICE_FILE, "w") as file:
        json.dump(invoices, file, indent=4)


# Load products
def load_products():

    if os.path.exists(PRODUCT_FILE):

        with open(PRODUCT_FILE, "r") as file:

            try:
                return json.load(file)

            except json.JSONDecodeError:
                return []

    return []


# Write products
def write_products(products):

    with open(PRODUCT_FILE, "w") as file:
        json.dump(products, file, indent=4)