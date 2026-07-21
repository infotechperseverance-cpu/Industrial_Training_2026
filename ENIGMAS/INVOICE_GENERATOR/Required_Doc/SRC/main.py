from Connetion_Module import connection, create_tables
import LoginAuthentication
import customermanagement
import Module3_ProductManagement
import Module4_InvoiceGeneration
import Module5_PdfInvoice
import search_invoice
import Returns_and_returnsHistory
import sales_dashboard
import invoice_pdf_sender

# Database Connection
conn = connection()

if conn is None:
    print("Database Connection Failed")
    exit()

create_tables()


# Login
logged_in_user = LoginAuthentication.login()

if not logged_in_user:
    print("Login Failed")
    conn.close()
    exit()


# Main Menu
while True:

    print("\n========== MAIN MENU ==========")
    print("1. Customer Management")
    print("2. Product Management")
    print("3. Generate Invoice")
    print("4. Search Invoice / Return")
    print("5. Sales Dashboard")
    print("6. Exit")

    choice = input("Enter Choice : ")

    if choice == "1":

        customermanagement.customer_menu()

    elif choice == "2":

        Module3_ProductManagement.product_menu(conn)

    elif choice == "3":

        invoice_id = Module4_InvoiceGeneration.invoice_generation(conn, logged_in_user)

        if invoice_id is not None:

            pdf_path = Module5_PdfInvoice.pdfInvoice(conn, invoice_id)

            cursor = conn.cursor()

            cursor.execute("""
                SELECT customers.email
                FROM invoices
                JOIN customers
                ON invoices.customer_id = customers.customer_id
                WHERE invoice_id=%s
            """, (invoice_id,))

            email = cursor.fetchone()[0]

            cursor.close()

            status = invoice_pdf_sender.send_invoice(email, pdf_path)

        if status:

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE invoices
            SET email_status='Sent'
            WHERE invoice_id=%s
            """,(invoice_id,))

            conn.commit()

            cursor.close()
    elif choice == "4":
        invoice_id = search_invoice.search_invoice()

        if invoice_id:
            Returns_and_returnsHistory.returns(invoice_id)
    elif choice == "5":

        while True:

            print("\n===== SALES DASHBOARD =====")
            print("1. Show Graph")
            print("2. Generate Report")
            print("3. Back")

            dashboard_choice = input("Enter Choice : ")

            if dashboard_choice == "1":
                sales_dashboard.graph()

            elif dashboard_choice == "2":
                sales_dashboard.generate_simple_report()

            elif dashboard_choice == "3":
                break

            else:
                print("Invalid Choice")

    elif choice == "6":

        conn.close()
        print("Thank You For Visiting Our Store!")
        break

    else:

        print("Invalid Choice")