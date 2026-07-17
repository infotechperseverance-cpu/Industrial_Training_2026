

import os
import shutil
from datetime import datetime
import time
'''
@Function Name : synchronize_folders
@Description   : This function synchronizes files between source and
                 destination folders. It copies newly added files,
                 updates modified files, and displays synchronization
                 status after completion.
@Input Param   : source_folder (Source folder path)
                 destination_folder (Destination folder path)
@Output Param  : Displays synchronization status
@Author        : Mamata Chaudhari
'''
def synchronize_folders():

    source_folder = input("Enter Source Folder Path : ").strip()
    destination_folder = input("Enter Destination Folder Path : ").strip()

    if not os.path.exists(source_folder):
        print("Source Folder Not Found.")
        return

    if not os.path.exists(destination_folder):
        print("Destination Folder Not Found.")
        return
     #--Variables to store synchronization summary
    total_files = 0
    copied_files = 0
    updated_files = 0
    #--Get all files from source folder
    files = os.listdir(source_folder)

    for file in files:

        source_file = os.path.join(source_folder, file)

        # Skip folders
        if not os.path.isfile(source_file):
            continue
        #--Create complete destination file path
        destination_file = os.path.join(destination_folder, file)

        total_files += 1

        if not os.path.exists(destination_file):

            copy_new_files(source_file, destination_file)

            copied_files += 1

        else:

            if update_modified_files(source_file,destination_file):

                updated_files += 1
    
    show_sync_status(
        total_files,
        copied_files,
        updated_files
    )

'''
@Function Name : copy_new_files
@Description   : This function copies a new file from the source folder
                 to the destination folder when the file does not exist
                 in the destination folder.
@Input Param   : source_file (Source file path)
                 destination_file (Destination file path)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def copy_new_files(source_file, destination_file):

    shutil.copy2(source_file, destination_file)

    print(os.path.basename(source_file),
          "Copied Successfully.")

'''
@Function Name : update_modified_files
@Description   : This function checks whether the source file has been
                 modified. If the source file is newer than the
                 destination file, it updates the destination file.
@Input Param   : source_file (Source file path)
                 destination_file (Destination file path)
@Output Param  : True (File updated)
                 False (No update required)
@Author        : Mamata Chaudhari
'''
def update_modified_files(source_file, destination_file):

    source_time = os.path.getmtime(source_file)

    destination_time = os.path.getmtime(destination_file)
    #--Check whether source file is newer
    if source_time > destination_time:

        shutil.copy2(source_file, destination_file)

        print(os.path.basename(source_file),"Updated Successfully.")
        return True

    return False

'''
@Function Name : show_sync_status
@Description   : This function displays synchronization details such as
                 total files checked, copied files, updated files,
                 synchronization time, and status.
@Input Param   : total_files (Total files checked)
                 copied_files (Number of copied files)
                 updated_files (Number of updated files)
@Output Param  : Displays synchronization status
@Author        : Mamata Chaudhari
'''
def show_sync_status(total_files,
                     copied_files,
                     updated_files):
    #--Display synchronization report
    print("\n===== SYNC STATUS =====\n")

    print("Total Files Checked :", total_files)

    print("Files Copied        :", copied_files)

    print("Files Updated       :", updated_files)

    print("Last Sync Time      :", datetime.now())

    print("Status              : SUCCESS")

'''
@Function Name : auto_sync
@Description   : This function automatically synchronizes files between
                 source and destination folders at fixed intervals.
                 The synchronization process continues until the user
                 stops it using Ctrl + C.
@Input Param   : source_folder (Source folder path)
                 destination_folder (Destination folder path)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def auto_sync():

    source_folder = input("Enter Source Folder Path : ").strip()

    destination_folder = input("Enter Destination Folder Path : ").strip()

    if not os.path.exists(source_folder):
        print("Source Folder Not Found.")
        return

    if not os.path.exists(destination_folder):
        print("Destination Folder Not Found.")
        return

    print("\nAuto Synchronization Started...")
    print("Press Ctrl + C To Stop Auto Synchronization")

    try:
        #--Run synchronization continuously
        while True:

            files = os.listdir(source_folder)

            for file in files:

                source_file = os.path.join(source_folder,file)
                #--Ignore folders
                if not os.path.isfile(source_file):
                    continue

                destination_file = os.path.join(destination_folder,file)
                #--Copy newly added file
                if not os.path.exists(destination_file):

                    copy_new_files(source_file,destination_file)

                else:
                    #--Update modified file
                    update_modified_files(source_file,destination_file)

            time.sleep(5)

    except KeyboardInterrupt:

        print("\nAuto Synchronization Stopped.")

'''
@Function Name : main
@Description   : This is the main driver function of the Folder
                 Synchronization module. It displays the menu,
                 accepts user choices, and calls the appropriate
                 function based on the selected option.
@Input Param   : None
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def main():

    while True:

        print("\n" + "=" * 40)
        print("    FOLDER SYNCHRONIZATION")
        print("=" * 40)

        print("1. Synchronize Folders")
        print("2. Auto Synchronization")
        print("3. Exit")

        choice = input("\nEnter Your Choice : ")

        if choice == "1":
            synchronize_folders()

        elif choice == "2":
            auto_sync()

        elif choice == "3":
            print("Thank You...")
            break

        else:
            print("Invalid Choice! Please Try Again.")


if __name__ == "__main__":
    main()                            

