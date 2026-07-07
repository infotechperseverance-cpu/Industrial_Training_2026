import os
import json
import shutil
from datetime import datetime

from Classify_file import load_data

LOG_FILE = "backup_log.json"


# ---------------- Load Backup Logs ----------------

def load():

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as file:
            return json.load(file)

    return {"backups": []}


# ---------------- Save Backup Logs ----------------

def save(data):

    with open(LOG_FILE, "w") as file:
        json.dump(data, file, indent=4)


# ---------------- Create Backup Entry ----------------

def create_backup_record(filename,
                         category,
                         source,
                         destination,
                         status):

    logs = load()

    backup = {

        "backup_id": len(logs["backups"]) + 1,

        "file_name": filename,

        "category": category,

        "source_path": source,

        "backup_path": destination,

        "backup_date": datetime.now().strftime("%d-%m-%Y"),

        "backup_time": datetime.now().strftime("%H:%M:%S"),

        "file_size": os.path.getsize(source)
        if os.path.exists(source)
        else 0,

        "status": status

    }

    logs["backups"].append(backup)

    save(logs)

# ---------------- Backup One File ----------------

def backup_file():

    records = load_data()

    if not records:
        print("\nNo files found.")
        return

    print("\n========== AVAILABLE FILES ==========")

    for i, item in enumerate(records, start=1):
        print(f"{i}. {item['filename']} ({item['category']})")

    filename = input("\nEnter File Name to Backup: ").strip()

    # Automatically create backup folder
    project_folder = os.path.dirname(os.path.abspath(__file__))
    backup_folder = os.path.join(project_folder, "backup")
    os.makedirs(backup_folder, exist_ok=True)

    found = False

    for item in records:

        if item["filename"] == filename:

            category = item["category"]

            source = os.path.join(
                "File_Manager",
                category,
                filename
            )

            destination = os.path.join(
                backup_folder,
                filename
            )

            if not os.path.exists(source):

                print("Source file not found.")

                create_backup_record(
                    filename,
                    category,
                    source,
                    destination,
                    "Failed"
                )

                return

            if os.path.exists(destination):

                print("File already exists in backup folder.")

                create_backup_record(
                    filename,
                    category,
                    source,
                    destination,
                    "Skipped"
                )

                return

            try:

                shutil.copy2(source, destination)

                create_backup_record(
                    filename,
                    category,
                    source,
                    destination,
                    "Copied"
                )

                print("\nFile backed up successfully.")
                print("Backup Location :", backup_folder)

            except Exception as e:

                print("Backup Failed :", e)

                create_backup_record(
                    filename,
                    category,
                    source,
                    destination,
                    "Failed"
                )

            found = True
            break

    if not found:
        print("File record not found.")

# ---------------- Backup All Files ----------------

def backup_all_files():

    records = load_data()

    if not records:
        print("\nNo files available for backup.")
        return

    # Automatically create backup folder
    project_folder = os.path.dirname(os.path.abspath(__file__))
    backup_folder = os.path.join(project_folder, "backup")
    os.makedirs(backup_folder, exist_ok=True)

    copied = 0
    skipped = 0
    failed = 0

    for item in records:

        filename = item["filename"]
        category = item["category"]

        source = os.path.join(
            "File_Manager",
            category,
            filename
        )

        destination = os.path.join(
            backup_folder,
            filename
        )

        if not os.path.exists(source):

            print(filename, "-> Source File Not Found")

            create_backup_record(
                filename,
                category,
                source,
                destination,
                "Failed"
            )

            failed += 1
            continue

        if os.path.exists(destination):

            print(filename, "-> Already Exists")

            create_backup_record(
                filename,
                category,
                source,
                destination,
                "Skipped"
            )

            skipped += 1
            continue

        try:

            shutil.copy2(source, destination)

            print(filename, "-> Backup Successful")

            create_backup_record(
                filename,
                category,
                source,
                destination,
                "Copied"
            )

            copied += 1

        except Exception as e:

            print(filename, "-> Backup Failed")
            print(e)

            create_backup_record(
                filename,
                category,
                source,
                destination,
                "Failed"
            )

            failed += 1

    print("\n========== BACKUP SUMMARY ==========")
    print("Backup Folder :", backup_folder)
    print("Total Files   :", len(records))
    print("Copied Files  :", copied)
    print("Skipped Files :", skipped)
    print("Failed Files  :", failed)
    print("====================================")

# ---------------- Display Backup History ----------------

def display_backup_history():

    logs = load()

    if not logs["backups"]:
        print("\nNo Backup History Found.")
        return

    print("\n=============== BACKUP HISTORY ===============")

    for backup in logs["backups"]:

        print("--------------------------------------------")
        print("Backup ID   :", backup["backup_id"])
        print("File Name   :", backup["file_name"])
        print("Category    :", backup["category"])
        print("Status      :", backup["status"])
        print("Backup Date :", backup["backup_date"])
        print("Backup Time :", backup["backup_time"])
        print("File Size   :", backup["file_size"], "Bytes")
        print("--------------------------------------------")


# ---------------- Search Backup Record ----------------

def search_backup_record():

    logs = load()

    if not logs["backups"]:
        print("\nNo Backup History Found.")
        return

    filename = input("Enter File Name : ").strip()

    found = False

    for backup in logs["backups"]:

        if backup["file_name"] == filename:

            print("\n========== RECORD FOUND ==========")

            print("Backup ID   :", backup["backup_id"])
            print("File Name   :", backup["file_name"])
            print("Category    :", backup["category"])
            print("Status      :", backup["status"])
            print("Source Path :", backup["source_path"])
            print("Backup Path :", backup["backup_path"])
            print("Date        :", backup["backup_date"])
            print("Time        :", backup["backup_time"])
            print("File Size   :", backup["file_size"], "Bytes")

            found = True

    if not found:
        print("Backup Record Not Found.")


# ---------------- Delete Backup History ----------------

def delete_backup_history():
    logs = load()
    if not logs["backups"]:
        print("Backup History Already Empty.")
        return

    choice = input("Delete Complete Backup History? (Y/N): ").upper()
    if choice == "Y":
        with open(LOG_FILE, "w") as file:
            json.dump({"backups": []}, file, indent=4)

        project_folder = os.path.dirname(os.path.abspath(__file__))

        backup_folder = os.path.join(project_folder, "backup")
        
        if os.path.exists(backup_folder):
            for filename in os.listdir(backup_folder):
                file_path = os.path.join(backup_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting file {filename}: {e}")

        print("Backup History and Folder Deleted Successfully.")
    else:
        print("Operation Cancelled.")


# ---------------- Backup Menu ----------------

def backup_menu():

    while True:

        print("\n================ BACKUP MENU ================")
        print("1. Backup One File")
        print("2. Backup All Files")
        print("3. Display Backup History")
        print("4. Search Backup Record")
        print("5. Delete Backup History")
        print("6. Exit")

        try:
            choice = int(input("Enter Your Choice : "))
        except ValueError:
            print("Invalid Input")
            continue

        match choice:

            case 1:
                backup_file()

            case 2:
                backup_all_files()

            case 3:
                display_backup_history()

            case 4:
                search_backup_record()

            case 5:
                delete_backup_history()

            case 6:
                print("Returning To Main Menu...")
                break

            case _:
                print("Invalid Choice.")