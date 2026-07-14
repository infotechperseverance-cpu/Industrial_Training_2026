import smtplib
from email.message import EmailMessage
import os

'''
Function Name:send_invoice
Purpose:Read customer's email and send invoice.pdf to the that email
Input parameters :customer_email,file_path
output parameters :none

'''

def send_invoice(email,file_path):
    try:
        customer_email = email #customer email
    
        pdf_file = file_path #pdf path
    
        if not os.path.exists(pdf_file):
            print("PDF File Not Found")
            return False
    
        choice = input("Do you want to send Email? (Y/N) : ")
    
        if choice.lower() != "y":
            print("Email Cancelled")
            return False
        
     #Give sender's email
        sender_email = "patilharshwardhan218@gmail.com"
    
    #Give 16-digits email password
        app_password = "app_password"       
    
        msg = EmailMessage()
        msg["Subject"] = "Invoice from Enigmas Supermarket"
    
        msg["From"] = sender_email
        msg["To"] = customer_email
    
        msg.set_content("""
                Dear Customer,
                
                Thank you for shopping with us.
                
                Your invoice is attached with this email.
                
                Thank You,
                Enigmas Supermarket
                """)
                
        with open(pdf_file, "rb") as file:
            pdf_data = file.read()
    
            file_name = os.path.basename(pdf_file)
    
            msg.add_attachment(
                pdf_data,
                maintype="application",
                subtype="pdf",
                filename=file_name
            )
    
            server = smtplib.SMTP("smtp.gmail.com", 587)
    
            server.starttls()
    
            server.login(sender_email, app_password)
    
            server.send_message(msg)
    
            server.quit()
    
            print("\nEmail Sent Successfully")
            return True
    except KeyboardInterrupt:
        print("\nkeyboard innterrupt\n")
    except Exception as e:
        print("\nError :", e)
        return False