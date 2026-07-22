import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


'''
@Function Name: generate_invoice_pdf
@Description  : Fetches transactional information from MySQL for a given invoice_id,
                generates a styled PDF billing layout, saves it locally, and updates
                the database record with the file reference path.
@inputParam   : db_conn (Active MySQL Connection object)
                invoice_id (INT - The specific invoice ID to print)
@outParam     : pdf_path (STRING - The path to the saved document, or None if failed)
@Author       : Dimpal Rajput
'''
    
def pdfInvoice(db_conn, invoice_id):
    try:
       
        connection = db_conn
        cursor = connection.cursor(buffered=True)

        # 2. Get the main bill details and customer information
        customer_info = """
            SELECT invoices.invoice_id,
       invoices.invoice_date,
       invoices.subtotal,
       invoices.gst_amount,
       invoices.discount,
       invoices.total_amount,
       customers.customer_name,
       customers.mobile_no,
       customers.email,
       users.username
       FROM invoices
       JOIN customers
       ON invoices.customer_id = customers.customer_id
       JOIN users
       ON invoices.user_id = users.user_id
       WHERE invoices.invoice_id = %s
                """
        cursor.execute(customer_info, (invoice_id,))
        bill_data = cursor.fetchone()
        
        if bill_data is None:
            print("Error: Invoice ID not found in the database!")
            cursor.close()
            return None
        
        # Save each piece of database column information 
        bill_id = bill_data[0]
        bill_date = bill_data[1]
        subtotal_amt = float(bill_data[2])
        gst_amt = float(bill_data[3])
        discount_amt = float(bill_data[4])
        final_amt = float(bill_data[5])

        name = bill_data[6]
        phone = bill_data[7]
        email = bill_data[8]
        cashier_name = bill_data[9]

        # 3. Get all the product items bought under this invoice number
        product_item = """
            SELECT products.product_name, invoice_items.quantity, 
                   invoice_items.unit_price, invoice_items.gst_amount, 
                   invoice_items.total_price 
            FROM invoice_items 
            JOIN products ON invoice_items.product_id = products.product_id
            WHERE invoice_items.invoice_id = %s
        """
        cursor.execute(product_item, (invoice_id,))
        items_list = cursor.fetchall()

        # 4. Make a simple folder on the computer to store the invoices
        folder = "all_invoices"
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        pdf_path = folder + "/invoice_" + str(bill_id) + ".pdf"

        # 5. Initialize the ReportLab document page layout settings
        pdf_file = SimpleDocTemplate(pdf_path, pagesize=letter)
        page_elements = []
        text_styles = getSampleStyleSheet()

        title_font = text_styles['Heading1']
        body_font = text_styles['Normal']

        # Add Title text at the top of the page elements box
        page_elements.append(Paragraph("INVOICE REPORT", title_font))
        page_elements.append(Spacer(1, 15))

        # 6. Build the Customer Information text table block
        customer_table_data = [
        [Paragraph("<b>Invoice ID:</b> #" + str(bill_id), body_font),
        Paragraph("<b>Customer Name:</b> " + str(name), body_font)],

        [Paragraph("<b>Date:</b> " + str(bill_date), body_font),
        Paragraph("<b>Mobile No:</b> " + str(phone), body_font)],

        [Paragraph("<b>Cashier:</b> " + str(cashier_name), body_font),
        Paragraph("<b>Email:</b> " + str(email), body_font)]
]
        info_table = Table(customer_table_data, colWidths=[250, 250])
        page_elements.append(info_table)
        page_elements.append(Spacer(1, 20))

        # 7. Build the main Purchased Products  chart grid
        grid_data = [[
            Paragraph("<b>Product Name</b>", body_font), 
            Paragraph("<b>Quantity</b>", body_font), 
            Paragraph("<b>Unit Price</b>", body_font), 
            Paragraph("<b>GST Amt</b>", body_font), 
            Paragraph("<b>Total</b>", body_font)
        ]]

        # Loop through rows and paste strings directly into the product list 
        for row in items_list:
            grid_data.append([
                Paragraph(str(row[0]), body_font),
                Paragraph(str(row[1]), body_font),
                Paragraph("Rs. " + str(float(row[2])), body_font),
                Paragraph("Rs. " + str(float(row[3])), body_font),
                Paragraph("Rs. " + str(float(row[4])), body_font)
            ])
            
        products_table = Table(grid_data, colWidths=[180, 60, 80, 80, 80])
        
        # Design layout settings matching the basic tutorial grid tuples
        products_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, 'gray'),
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        page_elements.append(products_table)
        page_elements.append(Spacer(1, 20))

        # 8. Add the Final Mathematical Billing Totals Summary block
        summary_data = [
            [Paragraph("<b>Subtotal:</b>", body_font), "Rs. " + str(subtotal_amt)],
            [Paragraph("<b>GST Amount:</b>", body_font), "Rs. " + str(gst_amt)],
            [Paragraph("<b>Counter Discount:</b>", body_font), "Rs. " + str(discount_amt)],
            [Paragraph("<b>Grand Total:</b>", body_font), "Rs. " + str(final_amt)]
        ]
        totals_table = Table(summary_data, colWidths=[380, 100])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
            ('LINEABOVE', (0, 3), (-1, 3), 1, 'black')
        ]))
        page_elements.append(totals_table)

        # 9. Print out and build the final PDF report document file
        pdf_file.build(page_elements)
        print("Success: PDF Invoice saved at: " + pdf_path)

        # 10. Update the table path location string column row inside MySQL database
        save_query = "UPDATE invoices SET pdf_path = %s WHERE invoice_id = %s"
        cursor.execute(save_query, (pdf_path, invoice_id))
        connection.commit()
        
        cursor.close()
        return pdf_path

    except Exception as error:
        print("PDF Generation Error: " + str(error))
        return None