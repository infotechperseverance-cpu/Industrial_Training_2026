from file_utils import load_invoices

class CustomerIntelligence:

    
    #Create purchase summary
    def customer_intelligence(self,customer_id):
        invoices=load_invoices()
        total_invoices=0
        total_spent=0
        products={}
        discount=0

        for invoice_id,invoice in invoices.items():
            if invoice["customer_id"]==customer_id:

                total_invoices+=1
                total_spent+=invoice["total_price"]

                for item in invoice["items"]:
                    name=item["name"]

                    if name in products:
                        products[name]+=item["quantity"]

                    else:
                        products[name]=item["quantity"]


        if total_spent == 0:
            print("\n" + "=" * 50)
            print("        CUSTOMER PURCHASE SUMMARY")
            print("=" * 50)
            print(f"Customer ID      : {customer_id}")
            print("Purchase History : New Customer")
            print("Previous Spending: ₹0.00")
            print("Eligible Discount: 0%")
            print("=" * 50)
            return 0

        favourite_product=max(products,key=products.get)
        total_products=sum(products.values())

        print("\n"+"="*50)
        print("         CUSTOMER PURCHASE HISTROY")
        print("CUSTOMER ID =",customer_id)
        print("Total products :",total_products)
        print("Total invoices :",total_invoices)
        print("Total spent :",total_spent)
       

        if total_spent>10000:
            discount=int(input("Enter the discount percent:"))

        else:
            discount=0

        print("Eligible Discount :",discount,"%")
        print("="*50)

        return discount


