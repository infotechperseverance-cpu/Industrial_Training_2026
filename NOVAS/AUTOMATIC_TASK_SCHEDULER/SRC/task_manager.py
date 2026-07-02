import csv
import os

HEADER = ['Task ID', 'Task Name', 'Date', 'Time', 'Priority','Category','Status','Repeat']


# ---------------- DELETE TASK ----------------
def delete_task():

    with open('tasks.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        tasks = list(reader)

    if not tasks:
        print("No tasks available to delete.")
        return

    delete_id = input("Enter Task ID: ")

    deleted_tasks = []
    remaining_tasks = []

    for row in tasks:
        if row.get('Task ID') == delete_id:
            deleted_tasks.append(row)
        else:
            remaining_tasks.append(row)

    if not deleted_tasks:
        print("Task ID Not Found.")
        return

    # recycle bin write
    with open('recycle_bin.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)

        if os.stat("recycle_bin.csv").st_size == 0:
            writer.writeheader()

        for row in deleted_tasks:
            clean_row = {
                'Task ID': row.get('Task ID', ''),
                'Task Name': row.get('Task Name', ''),
                'Date': row.get('Date', ''),
                'Time': row.get('Time', ''),
                'Priority': row.get('Priority', ''),
                'Category': row.get('Category', ''),
                'Status': row.get('Status', ''),
                'Repeat': row.get('Repeat', ''),
            }
            writer.writerow(clean_row)

    # rewrite tasks
    with open('tasks.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(remaining_tasks)

    print("Task moved to recycle bin successfully.")


# ---------------- RESTORE TASK ----------------
def restore_deleted_task():

    with open('recycle_bin.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        tasks = list(reader)

    if not tasks:
        print("No deleted tasks available.")
        return

    restore_id = input("Enter Task ID to restore: ")

    restored_tasks = []
    remaining_tasks = []

    for row in tasks:
        if row.get('Task ID') == restore_id:
            restored_tasks.append(row)
        else:
            remaining_tasks.append(row)

    if not restored_tasks:
        print("Task ID Not Found.")
        return

    # restore to tasks.csv
    with open('tasks.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)

        if os.stat("tasks.csv").st_size == 0:
            writer.writeheader()
        for row in restored_tasks:
            row.pop(None, None)
        writer.writerows(restored_tasks)

    # update recycle bin
    with open('recycle_bin.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(remaining_tasks)

    print("Task restored successfully.")