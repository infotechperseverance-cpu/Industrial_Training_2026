from validatation import validate_name
from Classify_file import (
    create_file,
    rename_file,
    delete_file,
    display_records
)
from Password import password_protection
from backup import backup_menu
from file_sorting import sorting_menu
from file_history import show_history
from file_sizee import analyze
from Qrcode_gen import shareqr
from dublication_file import duplicate_file_management
from recycle import movetobin, restore_file,show_recycle_bin
while True:

    print("\n===================================================")
    print("          FILE MANAGEMENT SYSTEM"                     )
    print("=====================================================")
    print("1. Create File")
    print("2. Rename File")
    print("3. Delete File")
    print("4. Display File Records")
    print("5. Backup System")
    print("6. Sorting of files")
    print("7. File History")
    print("8. File size Analyser")
    print("9. Qrcode Generation for file sharing")
    print("10.Duplicate file Management")
    print("11.Show Recycle bin ")
    print("12.Restore file ")
    print("13. Exit")
    print("===================================================")

    try:
        choice = int(input("Enter Your Choice: "))
    except ValueError:
        print("Invalid Input! Please enter a number.")
        continue

    match choice:

        # ---------------- Create File ----------------

        case 1:

            filename = input("Enter File Name: ").strip()

            if validate_name(filename):

                success, password = password_protection()

                create_file(filename)

                if success:
                    print("Password Protection Enabled.")
                else:
                    print("Password Protection Skipped.")

        # ---------------- Rename File ----------------

        case 2:

            old_name = input("Enter Old File Name: ").strip()
            new_name = input("Enter New File Name: ").strip()

            if validate_name(new_name):
                rename_file(old_name, new_name)

        # ---------------- Delete File ----------------

        case 3:

            filename = input("Enter File Name to Delete: ").strip()

            delete_file(filename)

        # ---------------- Display Records ----------------

        case 4:

            display_records()

        # ---------------- Backup System ----------------

        case 5:

            backup_menu()


        case 6:
             sorting_menu()

        case 7:
             show_history()

        case 8:
             analyze()

        case 9:
             shareqr()

        case 10:
             duplicate_file_management()

        case 11:
             show_recycle_bin()

        case 12:
              filename = input("Enter File Name : ")
              restore_file(filename)


        



        # ---------------- Exit ----------------

        case 13:

            print("\nThank You For Using File Management System.")
            break

        # ---------------- Invalid Choice ----------------

        case _:

            print("Invalid Choice! Please Try Again.")