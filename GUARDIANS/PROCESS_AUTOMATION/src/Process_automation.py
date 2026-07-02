"""
Project Name : System Tracker Automation
Developed By : Guardians

Functions:
1. CPU Monitoring
2. RAM Monitoring
3. Disk Monitoring
4. Process Monitoring
5. Email Alerts
6. Daily Report
7. Graph Generation
"""

import os
import csv
import time
import psutil
from datetime import datetime, date, timedelta
import smtplib
import matplotlib.pyplot as plt
from email.message import EmailMessage

#Configuration Information

cpu_threshold = 2       
ram_threshold = 2               
monitor_interval= 5               
process_interval = 60            
time_data = []
cpu_data = []
ram_data = []
disk_data = []

CSV_DIR = "logs"
SYSTEM_LOG_CSV = os.path.join(CSV_DIR, "system_metrics.csv")
PROCESS_LOG_CSV = os.path.join(CSV_DIR, "process_log.csv")
DAILY_REPORT_DIR = CSV_DIR

smtp_server= "smtp.gmail.com"
smtp_port= 587
username= "darshanvyas862@gmail.com"
password= "vihs ocgi fcii lqap"
from_addr= "darshanvyas862@gmail.com"
to_addrs= ["vyasdarshan966@gmail.com"]


os.makedirs(CSV_DIR, exist_ok=True)

#csv files ensuration
def create_csv_files():
    if not os.path.exists(SYSTEM_LOG_CSV):
        with open(SYSTEM_LOG_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "cpu_percent", "ram_percent", "disk_total", "disk_used", "disk_free"])
    if not os.path.exists(PROCESS_LOG_CSV):
        with open(PROCESS_LOG_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "pid", "name", "cpu_percent", "memory_percent", "status", "num_threads"])

create_csv_files()

#alert checking
def check_alert(cpu_usage, ram_usage):
    alerts = []
    if cpu_usage >= cpu_threshold:
        alerts.append(f"WARNING: CPU Usage has exceeded {cpu_threshold}% (current: {cpu_usage}%)")
    if ram_usage >= ram_threshold:
        alerts.append(f"WARNING: RAM Usage has exceeded {ram_threshold}% (current: {ram_usage}%)")
    if not alerts:
        return "System running normally"
    return "\n".join(alerts)

# Email sent function 
def send_email(subject, body):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_addrs[0]
        msg.set_content(body)
        with smtplib.SMTP(smtp_server,smtp_port) as smtp:
            smtp.starttls()
            smtp.login(username,password)
            smtp.send_message(msg)
        print("Email was sent to appropriate email")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

#Monitoring of cpu,ram,disk
def system_monitoring():

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # CPU Monitoring
    cpu_percent = psutil.cpu_percent(interval=1)

    # RAM Monitoring
    ram_percent= psutil.virtual_memory().percent

    # Disk Monitoring
    disk = psutil.disk_usage('/')
    total_disk = round(disk.total / (1024**3), 2)  # GB
    used_disk = round(disk.used / (1024**3), 2)    # GB
    free_disk = round(disk.free / (1024**3), 2)    # GB

    record = {
        "timestamp": timestamp,
        "cpu_percent": cpu_percent,
        "ram_percent": ram_percent,
        "disk_total": total_disk,
        "disk_used": used_disk,
        "disk_free": free_disk
        }

    
    return record


    
def append_system_csv(record):
    try:
        with open(SYSTEM_LOG_CSV, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                record["timestamp"],
                record["cpu_percent"],
                record["ram_percent"],
                record["disk_total"],
                record["disk_used"],
                record["disk_free"]
            ])
    except Exception:
        print("Failed to write system CSV")

def monitor_process():
    
    print("=" * 100)
    print("               PROCESS MONITORING SYSTEM")
    print("=" * 100)

    print("Scan Time :", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print("Total Running Processes :", len(psutil.pids()))
    print("-" * 100)

    header = "{:<8} {:<30} {:<10} {:<12} {:<12} {:<10}"
    print(header.format("PID", "Process Name", "CPU %", "Memory %", "Status", "Threads"))

    print("-" * 100)

    process_list = []

    for process in psutil.process_iter(
        ['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'num_threads']
    ):
        try:
            process_list.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort by CPU Usage
    process_list.sort(key=lambda x: x['cpu_percent'], reverse=True)

    for p in process_list:

        cpu = p['cpu_percent']
        warning = "  HIGH" if cpu > 20 else ""

        print(
            "{:<8} {:<30} {:<10} {:<12.2f} {:<12} {:<10}{}".format(
                p['pid'],
                str(p['name'])[:28],
                cpu,
                p['memory_percent'],
                p['status'],
                p['num_threads'],
                warning
            )
        )
        
def save_process_data():
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'num_threads']):
            try:
                info = proc.info
                with open(PROCESS_LOG_CSV, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        timestamp,
                        info.get("pid"),
                        info.get("name"),
                        info.get("cpu_percent"),
                        info.get("memory_percent"),
                        info.get("status"),
                        info.get("num_threads")
                    ])
            except :
                print("Please  try again")
    except:
        print("Something went wrong")

def generate_graph():
    print("Collecting system data... (Press Ctrl+C to stop)")

    second = 0

    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            second += 1
            time_data.append(second)
            cpu_data.append(cpu)
            ram_data.append(ram)
            disk_data.append(disk)

            print(f"{second}s -> CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%")

    except KeyboardInterrupt:
        print("\nCtrl+C detected! Generating graph...")

        os.makedirs("graphs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"graphs/System_Usage_{timestamp}.png"

        plt.figure(figsize=(12, 6))

        plt.plot(time_data, cpu_data, label="CPU Usage", linewidth=2)
        plt.plot(time_data, ram_data, label="RAM Usage", linewidth=2)
        plt.plot(time_data, disk_data, label="Disk Usage", linewidth=2)

        plt.title("System Resource Usage")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Usage (%)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        plt.savefig(filename, dpi=300)
        plt.show()

        print(f"\nGraph saved as {filename}")

boot_time = psutil.boot_time()
def saveup_time(start_time, end_time):

    file_name = "logs/system_uptime_log.csv"

    try:

        file_exists = os.path.exists(file_name)

        with open(file_name, "a", newline="") as file:

            writer = csv.writer(file)

            if  file_exists:
                writer.writerow([
                    "Boot Time",
                    "Start Time",
                    "End Time",
                    "System Uptime",
                    "Program Runtime"
                ])

            uptime = end_time - datetime.fromtimestamp(boot_time)
            running_time = end_time - start_time

            writer.writerow([
                datetime.fromtimestamp(boot_time),
                start_time,
                end_time,
                uptime,
                running_time
            ])

        print("Data Saved Successfully")

    except Exception as e:
        print("Error:", e)

def daily_report(for_date= None):
    
    if for_date is None:
        for_date = date.today()
    date_str = for_date.strftime("%Y-%m-%d")
    cpu_vals, ram_vals, disk_vals = [], [], []
    try:
        with open(SYSTEM_LOG_CSV, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["timestamp"].startswith(date_str):
                        cpu_vals.append(float(row["cpu_percent"]))
                        ram_vals.append(float(row["ram_percent"]))
                        disk_vals.append(float(row["disk_used_gb"]))
                    
    except FileNotFoundError:
        print("System CSV not found for report generation")
        return None

    if not cpu_vals:
        print("No data for date ", date_str)
        return None

    report = {
        "date": date_str,
        "avg_cpu": sum(cpu_vals) / len(cpu_vals),
        "avg_ram": sum(ram_vals) / len(ram_vals),
        "avg_disk_used_gb": sum(disk_vals) / len(disk_vals),
        "max_cpu": max(cpu_vals),
        "max_ram": max(ram_vals),
        "samples": len(cpu_vals)
    }

    # Save report to a CSV file
    report_file = os.path.join(DAILY_REPORT_DIR, f"daily_report_{date_str}.csv")
    try:
        with open(report_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "avg_cpu", "avg_ram", "avg_disk_used_gb", "max_cpu", "max_ram", "samples"])
            writer.writerow([
                report["date"],
                round(report["avg_cpu"], 2),
                round(report["avg_ram"], 2),
                round(report["avg_disk_used_gb"], 2),
                round(report["max_cpu"], 2),
                round(report["max_ram"], 2),
                report["samples"]
            ])
        print("Daily report saved to ", report_file)

        # Prepare email body
        body = (
            f"Daily System Report for {report['date']}\n\n"
            f"Average CPU: {report['avg_cpu']:.2f}%\n"
            f"Average RAM: {report['avg_ram']:.2f}%\n"
            f"Average Disk Used: {report['avg_disk_used_gb']:.2f} GB\n"
            f"Max CPU: {report['max_cpu']:.2f}%\n"
            f"Max RAM: {report['max_ram']:.2f}%\n"
            f"Samples Collected: {report['samples']}\n\n"
            f"Report file saved at: {report_file}"
        )

        # Send email with summary
        send_email(f"Daily System Report - {report['date']}", body)

    except Exception:
        print("Failed to write daily report")

    return report

def log_main(cpu_usage,ram_usage,alert): 
     try: 
         date = datetime.now().strftime("%d-%m-%y") 
         file_name = f"system_log_{date}.csv" 
         file_exists = os.path.exists(file_name) 
         with open(file_name, "a", newline="") as file: 
             writer = csv.writer(file) 
             if  file_exists: 
                 writer.writerow( 
                 ["Date","Time", "CPU Usage", "RAM Usage","Alert"])
                 writer.writerow( [ 
                         datetime.now().strftime("%d-%m-%y"), 
                         datetime.now().strftime("%H:%M:%S"), 
                         cpu_usage, 
                         ram_usage, 
                     alert]  ) 
                 print("Log saved successfully") 
     except FileNotFoundError: 
         print("Error: File not found") 
     except PermissionError: 
         print("Error: File is open or permission denied") 
     except Exception as e: 
         print("Log Error:", e)

     
def main(mode):
    
    print("System Tracker Automation started in ", mode,"mode")
    start_time = datetime.now()
    last_snapshot_minute = -1
    try:
        if mode == "monitor":
            while True:
                # 1. Sample system metrics
                record = system_monitoring()
                append_system_csv(record)
                print("System metrics recorded")
                print("CPU Usage =", record["cpu_percent"], "%")
                print("RAM Usage =", record["ram_percent"], "%")
                print("Disk usage=", record["disk_used"],"%")
                
                # 2. check alert
                alert_msg = check_alert(record["cpu_percent"], record["ram_percent"])
                if "WARNING" in alert_msg:
                    print(alert_msg)
                    log_main(record["cpu_percent"],record["ram_percent"],alert_msg)
                    send_email("System Alert", alert_msg)
                    
                    
                # 3. Process data is stored after 5 minutes
                now = datetime.now()

                if now.minute != last_snapshot_minute:
                    if now.minute % 5 == 0:  # every 5 minutes
                        save_process_data()
                        print("Process data is taken")
                        last_snapshot_minute = now.minute

                

                # 4. Daily report is generated at midnight
                now = datetime.now()
                if now.hour == 23 and now.minute == 59:
                    report = daily_report()
                    if report:
                        print("Daily report generated and emailed for ", report["date"])

                # 5. Sleep until next monitoring cycle
                time.sleep(monitor_interval)

        elif mode == "process":
            monitor_process()   
            print("Process monitoring completed")

        elif mode == "graph":
            generate_graph()
            print("Graph generated successfully")

        else:
            print("Unknown mode:", mode)

    except KeyboardInterrupt:
        print("System Tracker Automation stopped by user")
    finally:
        end_time = datetime.now()
        saveup_time(start_time, end_time)
        print("System uptime and monitoring duration logged")
        
if __name__ == "__main__":
    
      print("1.Monitor")
      print("2.Process")
      print("3.graph")
    
try:
      choice=int(input("Enter your choice:"))

      if choice==1:
          main("monitor")

      elif choice==2:
         main("process")

      elif choice==3:
         main("graph")

      else:
          print("Invalid choice")

except:
    print("Enter a valid integer choice ") 
