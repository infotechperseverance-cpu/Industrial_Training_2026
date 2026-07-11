import os
from fiie_backup import Backup_File
from write_log import write_log

"""
Two ways to delete:
    delete_all(files)       - deletes every file in the list
    delete_selected(files)  - asks 'y' or 'n' for each file one by
                              one, then asks a final 'ok' to confirm
                              before anything is actually deleted
"""


def delete_all(files):
    for f in files:
        if not os.path.exists(f):
            continue

        name = os.path.basename(f)

        Backup_File(f)

        try:
            os.remove(f)
            print(f"{name} deleted (backed up first).")
            write_log(f"Deleted {name}", "SUCCESS")
        except Exception as e:
            print(f"Could not delete {name}:", e)
            write_log(f"Delete failed {name}", "FAILED")


def delete_selected(files):
    to_delete = []

    for f in files:
        if not os.path.exists(f):
            continue

        name = os.path.basename(f)
        choice = input(f"Delete {name}? (y/n): ").strip().lower()

        if choice == "y":
            to_delete.append(f)

    if not to_delete:
        print("No files selected for deletion.")
        return

    print("\nFiles selected for deletion:")
    for f in to_delete:
        print(" -", os.path.basename(f))

    confirm = input("\nEnter 'ok' to confirm deletion: ").strip().lower()

    if confirm != "ok":
        print("Deletion cancelled.")
        return

    for f in to_delete:
        name = os.path.basename(f)

        Backup_File(f)

        try:
            os.remove(f)
            print(f"{name} deleted (backed up first).")
            write_log(f"Deleted {name}", "SUCCESS")
        except Exception as e:
            print(f"Could not delete {name}:", e)
            write_log(f"Delete failed {name}", "FAILED")