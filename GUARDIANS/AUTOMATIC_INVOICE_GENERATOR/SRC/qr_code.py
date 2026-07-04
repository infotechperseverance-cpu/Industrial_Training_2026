import qrcode

class QRCodeGenerator:

    def generate_qr(self, invoice_id, invoice):

        qr_data = f"""
Invoice ID : {invoice_id}
Customer Name : {invoice['customer_name']}
Customer ID : {invoice['customer_id']}
Subtotal : ₹{invoice['subtotal']:.2f}
GST : ₹{invoice['GST']:.2f}
Discount : ₹{invoice['discount']:.2f}
Total Amount : ₹{invoice['total_price']:.2f}
"""

        qr = qrcode.make(qr_data)

        qr_file = f"{invoice_id}_qr.png"

        qr.save(qr_file)

        return qr_file