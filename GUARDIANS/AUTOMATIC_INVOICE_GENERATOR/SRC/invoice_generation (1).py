from file_utils import *

from customer_intelligence import *

class Automatic_invoice_generator:
    
    #generate invoices

    def invoice_generation(self,customer_id,customer_name):
        
        invoices=load_invoices()
        products = load_products()

        x=CustomerIntelligence()

        discount_percent=x.customer_intelligence(customer_id)

        items=[]
        
        invoice_id="INV"+str(len(invoices)+1).zfill(3)

        subtotal=0

        
        n=int(input("How many products:"))

        for i in range(n):

            print("-"*50)

            print("Product",i+1,":")

            product_id = input("Enter Product ID: ")
            print("Entered Product ID:", product_id)

            found = False

            for product in products:
                print("Checking:", product["id"], product["name"])

                if str(product["id"]) == product_id:
                    print("Matched:", product["name"])
                    found = True

                    item_name = product["name"]
                    price = product["price"]

                    print("Product Name :", item_name)
                    print("Price :", price)
                    print("Available Stock :", product["stock"])

                    quantity = int(input("Enter the quantity: "))

                    if quantity > product["stock"]:
                        print("Insufficient Stock")
                        break

                    total = quantity * price

                    subtotal += total

                    items.append({
                        "name": item_name,
                        "quantity": quantity,
                        "price": price,
                        "total": total
                    })

                    product["stock"] -= quantity

                    break

            if not found:
                print("Product Not Found")
           


        write_products(products)
        GST=0.18*subtotal

        discount=discount_percent/100*subtotal

        total_price=subtotal+GST-discount

        print("Invoice generated successfully")

       
        invoice={

           "customer_id":customer_id,

           "customer_name":customer_name,

           "items":items,

           "subtotal":subtotal,

           "GST":GST,

           "discount":discount,

           "total_price":total_price

           }

        invoices[invoice_id]=invoice

        write_invoices(invoices)

        print("Invoice generated successfully")
