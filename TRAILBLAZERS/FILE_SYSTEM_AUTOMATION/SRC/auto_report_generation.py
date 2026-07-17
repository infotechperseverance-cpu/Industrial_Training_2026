import csv
import os
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import ( SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer)

from database import get_connection


class AutomaticReportGeneration:

    '''
    @Function Name : __init__

    @Description   : Initializes database connection and creates
                     the Generated_Reports table.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()
        self.create_table()


    '''
    @Function Name : create_table

    @Description   : Creates the Generated_Reports table if it
                     does not already exist.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Generated_Reports(
                    report_id INT AUTO_INCREMENT PRIMARY KEY,
                    report_name VARCHAR(150),
                    report_type VARCHAR(50),
                    generated_by VARCHAR(100),
                    generated_date DATETIME,
                    report_status VARCHAR(30)
                )
            """)
            self.connection.commit()

        except Exception as error:
            print(f"\nDatabase Error : {error}")


    '''
    @Function Name : save_report

    @Description   : Saves generated report details into the
                     Generated_Reports table.

    @InputParam    : report_name
                     report_type
                     generated_by
                     status

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def save_report(self, report_name, report_type, generated_by="System", status="Generated"):
        try:
            query = """
                INSERT INTO Generated_Reports(
                    report_name,
                    report_type,
                    generated_by,
                    generated_date,
                    report_status
                )
                VALUES(%s,%s,%s,%s,%s)
            """

            values = (report_name, report_type, generated_by, datetime.now(), status)

            self.cursor.execute(query, values)
            self.connection.commit()

        except Exception as error:
            print(f"\nError : {error}")


    '''
    @Function Name : display_operation_history

    @Description   : Displays all file operations stored in the
                     File_Operations table.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def display_operation_history(self):
        try:
            self.cursor.execute("""
                SELECT *
                FROM File_Operations
                ORDER BY operation_time DESC
            """)

            records = self.cursor.fetchall()

            if not records:
                print("\nNo operation history found.")
                return

            print("\n" + "=" * 120)
            print(f"{'Module':25}{'Operation':25}{'Status':15}{'Date & Time':30}")
            print("=" * 120)

            for record in records:
                print(f"{record['module_name'][:25]:25}{record['operation_type'][:25]:25}{record['status']:15}{str(record['operation_time']):30}")

            print("=" * 120)

        except Exception as error:
            print(f"\nError : {error}")

    '''
    @Function Name : generate_daily_report

    @Description   : Generates and displays today's operations
                     from the File_Operations table.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def generate_daily_report(self):
        try:
            today = datetime.now().date()

            query = """
                SELECT *
                FROM File_Operations
                WHERE DATE(operation_time)=%s
            """

            self.cursor.execute(query, (today,))
            records = self.cursor.fetchall()

            if not records:
                print("\nNo records found.")
                return

            print("\n========== DAILY REPORT ==========\n")

            for record in records:
                print(f"Module      : {record['module_name']}")
                print(f"Operation   : {record['operation_type']}")
                print(f"File        : {record['file_name']}")
                print(f"Status      : {record['status']}")
                print(f"Time        : {record['operation_time']}")
                print("-" * 50)

            print("\nDaily Report Generated Successfully.")

            while True:

                print("\n1. Download PDF")
                print("2. Exit")

                choice = input("Enter Choice : ")

                if choice == "1":

                    self.generate_pdf(records, "Daily")

                    break

                elif choice == "2":

                    break

                else:

                    print("\nInvalid Choice.")

        except Exception as error:
            print(f"\nError : {error}")


    '''
    @Function Name : generate_weekly_report

    @Description   : Generates and displays operations
                     performed during the last seven days.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def generate_weekly_report(self):
        try:
            start_date = datetime.now() - timedelta(days=7)

            query = """
                SELECT *
                FROM File_Operations
                WHERE operation_time >= %s
                ORDER BY operation_time DESC
            """

            self.cursor.execute(query, (start_date,))
            records = self.cursor.fetchall()

            if not records:
                print("\nNo records found.")
                return

            print("\n========== WEEKLY REPORT ==========\n")

            for record in records:
                print(f"Module    : {record['module_name']}")
                print(f"Operation : {record['operation_type']}")
                print(f"File      : {record['file_name']}")
                print(f"Status    : {record['status']}")
                print(f"Time      : {record['operation_time']}")
                print("-" * 50)

            print("\nWeekly Report Generated Successfully.")

            while True:

                print("\n1. Download PDF")
                print("2. Exit")

                choice = input("Enter Choice : ")

                if choice == "1":

                    self.generate_pdf(records, "Weekly")

                    break

                elif choice == "2":

                    break

                else:

                    print("\nInvalid Choice.")

        except Exception as error:
            print(f"\nError : {error}")

    '''
    @Function Name : generate_monthly_report

    @Description   : Generates and displays operations
                     performed during the last thirty days.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def generate_monthly_report(self):
        try:
            start_date = datetime.now() - timedelta(days=30)

            query = """
                SELECT *
                FROM File_Operations
                WHERE operation_time >= %s
                ORDER BY operation_time DESC
            """

            self.cursor.execute(query, (start_date,))
            records = self.cursor.fetchall()

            if not records:
                print("\nNo records found.")
                return

            print("\n========== MONTHLY REPORT ==========\n")

            for record in records:
                print(f"Module    : {record['module_name']}")
                print(f"Operation : {record['operation_type']}")
                print(f"File      : {record['file_name']}")
                print(f"Status    : {record['status']}")
                print(f"Time      : {record['operation_time']}")
                print("-" * 50)

            print("\nMonthly Report Generated Successfully.")

            while True:

                print("\n1. Download PDF")
                print("2. Exit")

                choice = input("Enter Choice : ")

                if choice == "1":

                    self.generate_pdf(records, "Monthly")

                    break

                elif choice == "2":

                    break

                else:

                    print("\nInvalid Choice.")

        except Exception as error:
            print(f"\nError : {error}")


    '''
    @Function Name : report_summary

    @Description   : Displays a summary of all operations
                     grouped by operation type.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def report_summary(self):
        try:
            self.cursor.execute("""
                SELECT
                    operation_type,
                    COUNT(*) AS total
                FROM File_Operations
                GROUP BY operation_type
            """)

            records = self.cursor.fetchall()

            if not records:
                print("\nNo records found.")
                return

            print("\n========== REPORT SUMMARY ==========\n")

            total = 0

            for record in records:
                print(f"{record['operation_type']:<35}{record['total']}")
                total += record["total"]

            print("-" * 45)
            print(f"Total Operations : {total}")

        except Exception as error:
            print(f"\nError : {error}")


    '''
    @Function Name : export_pdf

    @Description   : Exports all records from the File_Operations
                     table into a PDF report with report summary.

    @InputParam    : NONE

    @OutParam      : PDF File

    @Author        : Srushti Subhash Mahajan
    '''
    def generate_pdf(self, records, report_type):
        try:

            if not records:
                print("\nNo records available.")
                return

            filename = f"{report_type}_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

            pdf = SimpleDocTemplate(filename)

            elements = []

            styles = getSampleStyleSheet()

            title = Paragraph(
                f"""
                <para align="center">
                <font size="20"><b>FILE MANAGEMENT SYSTEM</b></font><br/><br/>
                <font size="16"><b>AUTOMATIC REPORT GENERATION</b></font><br/><br/>
                <font size="18"><b>{report_type.upper()} REPORT</b></font>
                </para>
                """,
                styles["Normal"]
            )

            elements.append(title)
            elements.append(Spacer(1, 20))

            info = Paragraph(
                f"""
                <b>Generated By :</b> System<br/>
                <b>Generated On :</b> {datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")}
                """,
                styles["Normal"]
            )

            elements.append(info)
            elements.append(Spacer(1, 15))

            summary_title = Paragraph(
                "<b><font size=14>REPORT SUMMARY</font></b>",
                styles["Heading2"]
            )

            elements.append(summary_title)
            elements.append(Spacer(1, 10))

            summary_query = """
                SELECT operation_type,
                    COUNT(*) AS total
                FROM File_Operations
                GROUP BY operation_type
            """

            self.cursor.execute(summary_query)

            summary_records = self.cursor.fetchall()

            order = [
                "Folder Selected",
                "Folder Scan",
                "Duplicate Scan",
                "Large File Scan",
                "Unused File Found",
                "Temporary File Scan",
                "Storage Statistics",
                "Free Storage Check",
                "Deletion Suggestion",
                "File Deleted"
            ]

            summary_data = [["Operation", "Count"]]

            total_operations = 0

            for operation in order:

                count = 0

                for record in summary_records:

                    if record["operation_type"] == operation:
                        count = record["total"]
                        break

                summary_data.append([
                    operation,
                    str(count)
                ])

                total_operations += count

            summary_data.append([
                "Total Operations",
                str(total_operations)
            ])

            summary_table = Table(
                summary_data,
                colWidths=[330, 90]
            )
            summary_table.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("BACKGROUND",(0,-1),(-1,-1),colors.lightgrey),
            ("GRID",(0,0),(-1,-1),1,colors.black),
            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
            ("ALIGN",(1,1),(-1,-1),"CENTER"),
            ("BOTTOMPADDING",(0,0),(-1,-1),6)
            ]))

            elements.append(summary_table)
            elements.append(Spacer(1,20))

            details_title = Paragraph(
                "<b><font size=14>OPERATION DETAILS</font></b>",
                styles["Heading2"]
            )

            elements.append(details_title)
            elements.append(Spacer(1,10))

            table_data = [[
                "Module",
                "Operation",
                "File Name",
                "Status",
                "Date & Time"
            ]]

            for record in records:

                table_data.append([
                    record["module_name"],
                    record["operation_type"],
                    record["file_name"] if record["file_name"] else "-",
                    record["status"],
                    str(record["operation_time"])
                ])

            report_table = Table(
                table_data,
                colWidths=[120,120,120,60,120]
            )

            report_table.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,0),colors.grey),
                ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                ("GRID",(0,0),(-1,-1),1,colors.black),
                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                ("BOTTOMPADDING",(0,0),(-1,0),8),
                ("BACKGROUND",(0,1),(-1,-1),colors.beige)
            ]))

            elements.append(report_table)
            elements.append(Spacer(1,15))

            footer = Paragraph(
                "<para align='center'><b>************ END OF REPORT ************</b></para>",
                styles["Normal"]
            )

            elements.append(footer)

            pdf.build(elements)

            self.save_report(
                filename,
                "PDF"
            )

            print("\nPDF Generated Successfully.")
            print(f"File : {filename}")

        except Exception as error:
            print(f"\nError : {error}")
            
        '''
        @Function Name : close_connection

        @Description   : Closes the database cursor and connection.

        @InputParam    : NONE

        @OutParam      : NONE

        @Author        : Srushti Subhash Mahajan
        '''

    def close_connection(self):
            try:
                if self.cursor:
                    self.cursor.close()

                if self.connection:
                    self.connection.close()

            except Exception:
                pass


    '''
    @Function Name : menu

    @Description   : Displays the Automatic Report Generation
                     menu and performs the selected operation.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def menu(self):

        while True:

            print("\n" + "=" * 50)
            print("      AUTOMATIC REPORT GENERATION")
            print("=" * 50)
            print("1. Display Operation History")
            print("2. Generate Daily Report")
            print("3. Generate Weekly Report")
            print("4. Generate Monthly Report")
            print("5. Report Summary")
            print("6. Exit")
            print("=" * 50)

            choice = input("\nEnter Choice : ").strip()

            if choice == "1":
                self.display_operation_history()

            elif choice == "2":
                self.generate_daily_report()

            elif choice == "3":
                self.generate_weekly_report()

            elif choice == "4":
                self.generate_monthly_report()

            elif choice == "5":
                self.report_summary()

            elif choice == "6":
                self.close_connection()
                print("\nThank You!")
                break

            else:
                print("\nInvalid Choice.")

# ---------------------------------------------
# Main Function
# ---------------------------------------------

if __name__ == "__main__":

    try:
        report = AutomaticReportGeneration()
        report.menu()

    except KeyboardInterrupt:
        print("\nProgram Interrupted.")

    except Exception as error:
        print(f"\nUnexpected Error : {error}")

