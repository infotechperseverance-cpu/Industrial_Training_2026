import json
import smtplib
from email.message import EmailMessage
import os

class InvoiceManager:
    def __init__(self,customer_file):
        self.customer_file = customer_file
    
# email sending module
    def email_sending(self,sender,  password,   customer_id,   pdf_file):
        try:
            print("Reading file:", os.path.abspath(self.customer_file))
            with open(   self.customer_file,   "r") as file:
                customers = json.load(file)
                customer_found = False

            print("Invoice Customer ID:", customer_id)

            for customer in customers:
                print("Customer JSON ID:", customer["customer_id"])
            
                if str(customer["customer_id"]) == str(customer_id):
                    customer_found = True
                    receiver = customer["email"]
                    msg = EmailMessage()
                    msg["Subject"] = "Invoice"
                    msg["From"] = sender
                    msg["To"] = receiver
                    msg.set_content(  "Please find attached invoice.")

                    with open(  pdf_file,    "rb") as file:
                        data = file.read()
                        msg.add_attachment( data,   maintype="application",   subtype="pdf",   filename=pdf_file )
                        server = smtplib.SMTP(  "smtp.gmail.com",  587 )
                        server.starttls()
                        server.login(     sender,password   )
                        server.send_message( msg )
                        server.quit()
                        print("Email Sent Successfully" )
                        break

            if customer_found is False:
                print(    "Customer Not Found" )

        except FileNotFoundError:
            print( "Customer File Not Found" )

        except smtplib.SMTPAuthenticationError:
            print( "Invalid Email or Password" )

        except smtplib.SMTPException as e:
            print("SMTP Error:",     e  )

        except Exception as e:
            print(  "Error:",   e )
# #create object
# obj = InvoiceManager(    "customer.json",   )

# #method call
# try:
#     with open("invoices.json", "r") as file:
#        invoices = json.load(file)

#     for invoice_id, invoice in invoices.items():

#         customer_id = invoice["customer_id"]

#         obj.email_sending(
#             sender="pratimakadam308@gmail.com",
#             password="srfv fhoe vnal kqeo",
#             customer_id=customer_id,
#             pdf_file=f"{invoice_id}.pdf"
#         )

# except json.JSONDecodeError:
#      print( "Invalid JSON File" )