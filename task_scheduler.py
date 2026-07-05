from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

# Store task history
task_history = []

# Function to execute task
def execute_task(task_name):
    start_time = datetime.now()

    status = "Running"
    print("\n--------------------------")
    print("Task Started")
    print("Task :", task_name)
    print("Start Time :", start_time)

    try:
        # Simulate task
        time.sleep(3)

        status = "Completed"

    except:
        status = "Failed"

    end_time = datetime.now()

    print("End Time :", end_time)
    print("Status :", status)

    task_history.append({
        "Task": task_name,
        "Start": start_time.strftime("%H:%M:%S"),
        "End": end_time.strftime("%H:%M:%S"),
        "Status": status
    })


# Scheduler
scheduler = BackgroundScheduler()

# Run every 20 seconds
scheduler.add_job(
    execute_task,
    "interval",
    seconds=20,
    args=["Automatic Backup"]
)

scheduler.start()

print("Automatic Task Scheduler Started...\n")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    scheduler.shutdown()

    print("\n========== TASK REPORT ==========")

    total = len(task_history)
    completed = 0
    failed = 0

    for task in task_history:

        print("-------------------------")
        print("Task :", task["Task"])
        print("Start :", task["Start"])
        print("End :", task["End"])
        print("Status :", task["Status"])

        if task["Status"] == "Completed":
            completed += 1
        else:
            failed += 1

    print("\n========== SUMMARY ==========")
    print("Total Tasks :", total)
    print("Completed :", completed)
    print("Failed :", failed)