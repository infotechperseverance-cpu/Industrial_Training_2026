from user_input import add_task, view_task, mark_task_completed
from record_due_tasks import view_tasks_due_today, view_overdue_tasks
from task_manager import delete_task, restore_deleted_task
from File_Manager import archive_tasks, backup_tasks, restore_tasks, sort_tasks
from statistics import display_statistics
from recurring_task import recurring_tasks
from reminder_notification import notify_type, check_reminders
from reminder_interval_task import Take_remainder_interval, set_remainder
from filter_tasks import filter_tasks
from update_task import update_task_details
import threading

# Start reminder threads
thread = threading.Thread(target=check_reminders, daemon=True)
thread.start()

thread2 = threading.Thread(target=set_remainder, daemon=True)
thread2.start()

while True:

    print("\n===== TASK SCHEDULER =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. View Tasks Due Today")
    print("4. View Overdue Tasks")
    print("5. Mark Task Completed")
    print("6. Filter Task")
    print("7. Update Task Details")
    print("8. Delete Task")
    print("9. Restore Deleted Task")
    print("10. Archive Completed Tasks")
    print("11. Backup Tasks")
    print("12. Restore Backup")
    print("13. Sort Tasks")
    print("14. Recurring Task")
    print("15. Notify Type")
    print("16. Reminder Interval")
    print("17. Statistics")
    print("18. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        view_task()

    elif choice == "3":
        view_tasks_due_today()

    elif choice == "4":
        view_overdue_tasks()

    elif choice == "5":
        mark_task_completed()

    elif choice == "6":
        filter_tasks()

    elif choice == "7":
       update_task_details()

    elif choice == "8":
       delete_task()

    elif choice == "9":
       restore_deleted_task()

    elif choice == "10":
       archive_tasks()

    elif choice == "11":
        backup_tasks()

    elif choice == "12":
        restore_tasks()

    elif choice == "13":
        sort_tasks()

    elif choice == "14":
        recurring_tasks()

    elif choice == "15":
        notify_type()

    elif choice == "16":
        Take_remainder_interval()

    elif choice == "17":
        display_statistics()

    elif choice == "18":
        print("Thank You!")
        break

    else:
        print("Invalid Choice")