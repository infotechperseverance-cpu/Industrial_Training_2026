import csv
import os
from datetime import datetime


FILE = "tasks.csv"
BACKUP_FILE = "backup.csv"
ARCHIVE_FILE = "archive.csv"


HEADER = ['Task ID', 'Task Name', 'Date', 'Time', 'Priority', 'Category', 'Status', 'Repeat']


# ---------------- CREATE BACKUP FILE IF NOT EXISTS ----------------
def ensure_file(file_name):
    if not os.path.exists(file_name):
        with open(file_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)


# ---------------- ARCHIVE COMPLETED TASKS ----------------
def archive_tasks():

    ensure_file(ARCHIVE_FILE)

    with open(FILE, 'r', newline="") as file:
        reader = csv.DictReader(file)
        tasks = list(reader)

    archived = []
    active = []

    for row in tasks:
        if row['Status'] == "Completed":
            archived.append(row)
        else:
            active.append(row)

    if not archived:
        print("No completed tasks to archive.")
        return

    # write archive
    with open(ARCHIVE_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerows(archived)

    # rewrite active tasks
    with open(FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(active)

    print("Archive completed.")


# ---------------- BACKUP TASKS ----------------
def backup_tasks():

    ensure_file(BACKUP_FILE)

    all_tasks = []

    # Read active tasks
    if os.path.exists(FILE):
        with open(FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            all_tasks.extend(reader)

    # Read archived tasks
    if os.path.exists("archive.csv"):
        with open("archive.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            all_tasks.extend(reader)

    if not all_tasks:
        print("No tasks to backup.")
        return

    # Write backup
    with open(BACKUP_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(all_tasks)

    print("Backup completed.")

# ---------------- RESTORE TASKS ----------------
def restore_tasks():

    if not os.path.exists(BACKUP_FILE):
        print("Backup file not found.")
        return

    with open(BACKUP_FILE, 'r', newline="") as file:
        reader = csv.DictReader(file)
        tasks = list(reader)

    if not tasks:
        print("Backup is empty.")
        return

    with open(FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(tasks)

    print("Restore completed.")


# ---------------- SORT TASKS ----------------
def get_datetime(task):
    return datetime.strptime(
        task['Date'] + " " + task['Time'],
        "%Y-%m-%d %I:%M %p"
    )

def sort_tasks():

    with open("tasks.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        tasks = list(reader)

    if not tasks:
        print("No tasks available.")
        return

    tasks.sort(key=get_datetime)

    with open("tasks.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(tasks)

    print("Tasks sorted successfully.")