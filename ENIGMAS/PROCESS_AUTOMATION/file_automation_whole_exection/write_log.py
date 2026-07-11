import os
import csv
from datetime import datetime
def write_log(action, status):

    file_name = "system_log.csv"
    file_exists = os.path.exists(file_name)
    import csv

    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Date", "Time", "Action", "Status"])

        now_date = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M:%S")
        
        writer.writerow([now_date, now_time, action, status])

    
