import os
import shutil
from datetime import datetime

from write_log import write_log
from scanner import scan_folder
from FIle_type_checking import check_file_type
from file_duplicate_checker import duplication_files_detection
from fiie_backup import Backup_File, Restore_File, destination_file
from search import search_file
from authantication import login
from selection import select_folder
from automatic_folder import mk
from file_renaming import rename_duplicates
from genearte_report import generate_report
from deleting import *

def delete_menu(files):
    while True:
        print("\n---- DELETE FILES ----")
        print("1. Delete All")
        print("2. Select Files to Delete")
        print("3. Back to Main Menu")
 
        choice = input("Choice: ").strip()
 
        match choice:
            case "1":
                if not files:
                    print("Scan a folder first (option 2).")
                else:
                    delete_all(files)
 
            case "2":
                if not files:
                    print("Scan a folder first (option 2).")
                else:
                    delete_selected(files)
 
            case "3":
                break
 
            case _:
                print("Invalid choice.")

def backup_menu():
    while True:
        print("\n---- BACKUP & RESTORE ----")
        print("1. Backup a File")
        print("2. Restore a File")
        print("3. List Backed Up Files")
        print("4. Back to Main Menu")

        choice = input("Choice: ").strip()

        match choice:
            case "1":
                path = input("File to backup: ").strip()
                Backup_File(path)

            case "2":
                name = input("Enter backed up file name to restore: ").strip()
                Restore_File(name)

            case "3":
                if os.path.isdir(destination_file):
                    files = [f for f in os.listdir(destination_file) if f != "backup_metadata.json"]
                    if files:
                        for f in files:
                            print(" -", f)
                    else:
                        print("No files backed up yet.")
                else:
                    print("No files backed up yet.")

            case "4":
                break

            case _:
                print("Invalid choice.")


def main():
    print("=== FILE ORGANIZER SYSTEM ===")

    '''if not login():
        print("Login failed. Exiting.")
        return'''

    source_folder = None
    files = []

    while True:
        print("=" *35)
        print("\n1. Select Folder")
        print("2. Scan & Detect Files")
        print("3. Create Folders")
        print("4. Move Files")
        print("5. Rename Duplicates")
        print("6. Backup File")
        print("7. Generate Report")
        print("8. Search File")
        print("9.delete file")
        print("10. Exit")
        print("="*35)
        
        choice = input("Choice: ").strip()


        match choice:
            case "1":
                source_folder = select_folder()
                write_log("selection","success")

            case "2":
                if source_folder:
                    files = scan_folder(source_folder)
                    for f in files:
                        print(os.path.basename(f), "->", check_file_type(f))
                else:
                    print("Select a folder first.")

            case "3":
                mk()

            case "4":
                if not files:
                    print("Scan a folder first (option 2).")
                    continue

                target = input("Move all files to which folder: ").strip()

                if not target or not os.path.exists(target):
                    print("That folder does not exist.")
                    continue

                for f in files:
                    name = os.path.basename(f)

                    if duplication_files_detection(target, f):
                        print(f"{name} already exists in {target}, skipped.")
                        continue

                    Backup_File(f)

                    shutil.move(f, os.path.join(target, name))
                    write_log(f"Moved {name}", "SUCCESS")
                    print(f"{name} moved to {target}")

            case "5":
                #print("selected folder")
                
                if source_folder:
                    folder = select_folder()
                    rename_duplicates(folder)
                    
                else:
                    print("select folder first")

            case "6":
                backup_menu()

            case "7":
                records = []
                while True:
                    file_name = input("Enter file name: ")
                    category = input("Enter category: ")
                    status = input("Enter status: ")
                    records.append([file_name, category, status, datetime.now()])
                    more = input("Add another record? (yes/no): ").strip().lower()
                    if more != "yes":
                        break
                generate_report(records)

            case "8":
                folder = input("Search in folder: ").strip()
                name = input("Filename: ").strip()
                search_file(folder, name)
                write_log(f"searched {name}", "SUCCESS")

            case "9":
                if source_folder:
                    delete_menu(files)
                    
                else:
                    print("select folder first")

     

            case "10":
                print("Goodbye!")
                write_log(f" exit", "SUCCESS")
                break

            case _:
                print("Invalid choice.")


if __name__ == "__main__":
    main()