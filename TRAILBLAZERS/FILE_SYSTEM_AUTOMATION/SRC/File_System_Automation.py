"""
==============================================================
Project Name : File System Automation
Purpose      : Main Menu for File System Automation
Author       : TrailBlazers Team
==============================================================
"""

from Backup import main as backup_main
from duplicate_management import main as duplicate_main
from face_recognition_prg import main as face_main
from file_classification import main as classification_main
from file_password_protection import main as password_main
from file_recovery_system import main as recovery_main
from file_version_control import main as version_main
from folder_synchronization import main as sync_main
from smart_file_search import main as search_main
from storage_optimization import main as storage_main
from auto_report_generation import main as report_main


def main():

    while True:

        print("\n================================================")
        print("          FILE SYSTEM AUTOMATION")
        print("================================================")
        print("1. Face Recognition")
        print("2. Automatic Backup")
        print("3. Smart File Search")
        print("4. Folder Synchronization")
        print("5. Duplicate File Management")
        print("6. Automatic File Classification")
        print("7. File Version Control")
        print("8. File Recovery System")
        print("9. Storage Optimization")
        print("10. Automatic Report Generation")
        print("11. File Password Protection")
        print("0. Exit")
        print("================================================")

        choice = input("Enter Your Choice : ").strip()

        try:

            if choice == "1":
                face_main()

            elif choice == "2":
                backup_main()

            elif choice == "3":
                search_main()

            elif choice == "4":
                sync_main()

            elif choice == "5":
                duplicate_main()

            elif choice == "6":
                classification_main()

            elif choice == "7":
                version_main()

            elif choice == "8":
                recovery_main()

            elif choice == "9":
                storage_main()

            elif choice == "10":
                report_main()

            elif choice == "11":
                password_main()

            elif choice == "0":

                print("\n================================")
                print("Thank You For Using")
                print("File System Automation")
                print("================================")
                break

            else:

                print("\nInvalid Choice. Please Try Again.")

        except Exception as error:

            print("\nError :", error)


if __name__ == "__main__":
    main()