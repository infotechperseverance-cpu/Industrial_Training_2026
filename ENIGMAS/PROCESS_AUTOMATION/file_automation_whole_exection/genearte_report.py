import os
import csv
from datetime import datetime
from write_log import *

def generate_report(records):
    folder = "Reports"
    if not os.path.exists(folder):
        os.mkdir(folder)

    file_name = "Report_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    file_path = os.path.join(folder, file_name)

    with open(file_path, "w", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["File Name", "Category", "Status", "Date&Time"])

        for row in records:
            writer.writerow(row)

    print("Report generated successfully.")
    print("Report saved at ", file_path)
    write_log("CSV report generated", "SUCCESS")



