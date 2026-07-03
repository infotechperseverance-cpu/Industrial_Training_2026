from datetime import datetime

tasks = [
    {
        "id": 1,
        "title": "Complete Python Project",
        "status": "Pending",
        "due_date": "2026-07-05"
    },
    {
        "id": 2,
        "title": "Prepare Report",
        "status": "In Progress",
        "due_date": "2026-07-03"
    }
]

# Automatic Task Execution
today = datetime.today().strftime("%Y-%m-%d")

for task in tasks:
    if task["due_date"] <= today and task["status"] != "Completed":
        task["status"] = "Completed"

# Task Status Tracking
print("\n------ TASK STATUS ------")
for task in tasks:
    print(f"ID: {task['id']}")
    print(f"Task: {task['title']}")
    print(f"Status: {task['status']}")
    print(f"Due Date: {task['due_date']}")
    print("-" * 30)

# Reports
total = len(tasks)
completed = sum(1 for t in tasks if t["status"] == "Completed")
pending = sum(1 for t in tasks if t["status"] == "Pending")
progress = sum(1 for t in tasks if t["status"] == "In Progress")

print("\n====== REPORT ======")
print("Total Tasks :", total)
print("Completed   :", completed)
print("Pending     :", pending)
print("In Progress :", progress)