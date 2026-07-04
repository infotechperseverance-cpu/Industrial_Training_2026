import json
from reportlab.pdfgen import canvas
from datetime import datetime


class InvoiceManager:
    def __init__(self, invoice_file):
        self.invoice_file = invoice_file
    def pdf_generation(self, invoice_id):
        try:
            with open(self.invoice_file, "r") as file:
                invoices = json.load(file)

            invoice = invoices.get(invoice_id)

            if invoice is None:
                print("Invoice Not Found")
                return

            filename = f"{invoice_id}.pdf"
            pdf = canvas.Canvas(filename)

            # Title
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawCentredString(300, 810, "INVOICE")

            pdf.line(40, 795, 560, 795)

            
            #Shop Details
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawString(50, 770, "Guardians Grocery")

            pdf.setFont("Helvetica", 11)
            pdf.drawString(50, 752, "Jalgaon, Maharashtra")
            pdf.drawString(50, 735, "Phone : 9876543210")

          
            # Date & Time
            current_date = datetime.now().strftime("%d-%m-%Y")
            current_time = datetime.now().strftime("%I:%M:%S %p")

            pdf.drawString(380, 752, f"Date : {current_date}")
            pdf.drawString(380, 735, f"Time : {current_time}")

            
            # Customer Details
            pdf.rect(45, 640, 510, 70)

            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(60, 690, f"Invoice ID : {invoice_id}")

            pdf.setFont("Helvetica", 11)
            pdf.drawString(
                60,
                670,
                f"Customer Name : {invoice['customer_name']}"
            )
            pdf.drawString(
                330,
                670,
                f"Customer ID : {invoice['customer_id']}"
            )

            
            # Product Table
            pdf.setFont("Helvetica-Bold", 12)

            pdf.rect(45, 500, 510, 120)

            # Horizontal Line
            pdf.line(45, 595, 555, 595)

            # Vertical Lines
            pdf.line(200, 500, 200, 620)
            pdf.line(300, 500, 300, 620)
            pdf.line(420, 500, 420, 620)

            # Table Heading
            pdf.drawString(75, 603, "Product")
            pdf.drawString(220, 603, "Qty")
            pdf.drawString(330, 603, "Price")
            pdf.drawString(455, 603, "Total")

            y = 575

            pdf.setFont("Helvetica", 11)
            print(invoice["items"])
            for item in invoice["items"]:
                pdf.drawString(60, y, item["name"])
                pdf.drawString(230, y, str(item["quantity"]))
                pdf.drawString(330, y, f"{item['price']:.2f}")
                pdf.drawString(455, y, f"{item['total']:.2f}")
                y -= 20

                   
            # Bill Summary
            pdf.rect(320, 360, 235, 110)

            pdf.setFont("Helvetica", 11)

            pdf.drawString(
                335,
                445,
                f"Subtotal : ₹{invoice['subtotal']:.2f}"
            )

            pdf.drawString(
                335,
                425,
                f"GST : ₹{invoice['GST']:.2f}"
            )

            pdf.drawString(
                335,
                405,
                f"Discount : ₹{invoice['discount']:.2f}"
            )

            pdf.line(330, 390, 545, 390)

            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(
                335,
                370,
                f"Total Amount : ₹{invoice['total_price']:.2f}"
            )

            
            # Ending message
            pdf.setFont("Helvetica-Oblique", 12)
            pdf.drawCentredString(
                300,
                300,
                "Thank You!Please Visit Again!"
            )

            pdf.line(40, 285, 560, 285)

            pdf.save()

            print(f"PDF Generated Successfully : {filename}")

        except FileNotFoundError:
            print("Invoice File Not Found")

        except json.JSONDecodeError:
            print("Invalid JSON File")

        except Exception as e:
            print("Error:", e)


