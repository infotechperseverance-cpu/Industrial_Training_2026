import mysql.connector
import subprocess
import os
from datetime import datetime

# ---------------- DATABASE CONFIGURATION ----------------
HOST = "localhost"
USER = "root"
PASSWORD = "WJ28@krhps"
DATABASE = "task_scheduler_db"
BACKUP_FOLDER = "backups"

# ---------------- CREATE BACKUP FOLDER ----------------
def create_backup_folder():

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    # ---------------- CREATE DATABASE BACKUP ----------------
def create_backup():

    create_backup_folder()

    current_time = datetime.now().strftime("%Y-%m-%d_%H%M")

    backup_file = os.path.join(BACKUP_FOLDER,  f"backup_{current_time}.sql")

    command = [ "mysqldump", "-h", HOST,"-u", USER,"-p" + PASSWORD,DATABASE,"users","tasks" ]

    try:
        with open(backup_file, "w") as file:
            result = subprocess.run( command, stdout=file, stderr=subprocess.PIPE, text=True  )

        if result.returncode == 0:
            print("\nBackup created successfully.")
            print("Backup File:", backup_file)

        else:
            print("\nBackup failed.")
            print(result.stderr)

    except FileNotFoundError:
        print("\nError: mysqldump command not found.")

    except Exception as error:
        print("\nBackup Error:", error)
# ---------------- RESTORE DATABASE ----------------
def restore_backup():

    create_backup_folder()

    backups = [ file for file in os.listdir(BACKUP_FOLDER)
        if file.endswith(".sql") ]

    if not backups:
        print("\nNo backup files available.")
        return
    print("\nAvailable backups:")

    for index, backup in enumerate(backups, start=1):
        print(f"{index}. {backup}")

    # Select backup
    while True:
        try:
            choice = int(input("\nSelect a backup to restore: ")  )

            if 1 <= choice <= len(backups):
                selected_backup = backups[choice - 1]
                break

            else:
                print("\nInvalid backup selection.")

        except ValueError:
            print("\nPlease enter a valid number.")


    # Confirmation
    confirmation = input( "\nWARNING: This will overwrite your current " "database tables. Continue? (yes/no): "  ).lower()

    if confirmation != "yes":
        print("\nRestore cancelled.")
        return

    backup_path = os.path.join( BACKUP_FOLDER, selected_backup  )
    command = [ "mysql", "-h", HOST, "-u", USER, "-p" + PASSWORD, DATABASE ]

    try:
        with open(backup_path, "r") as file:
            result = subprocess.run( command, stdin=file, stderr=subprocess.PIPE, text=True )

        if result.returncode == 0:
            print( f"\nData restored successfully from " f"{selected_backup}.")

        else:
            print("\nRestore failed.")

            if ("Access denied" in result.stderr or "1045" in result.stderr ):
                print( "Database authentication error:Invalid MySQL username or password." )
                
            else:
                print(result.stderr)    
    


    except FileNotFoundError:
        print("\nError: mysql command not found.")

    except Exception as error:
        print("\nRestore Error:", error)

# ---------------- BACKUP & RESTORE MENU ----------------
while True:

    print("\n========== BACKUP & RESTORE ==========")
    print("1. Create Backup")
    print("2. Restore from Backup")
    print("3. Back to Main Menu")

    choice = input("\nEnter your choice: "  )

    if choice == "1":
        create_backup()

    elif choice == "2":
        restore_backup()

    elif choice == "3":
        print(  "\nReturning to Main Menu...")
        break

    else:
        print( "\nInvalid choice. Please try again." )
