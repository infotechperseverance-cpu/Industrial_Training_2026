'''
Duplicate File Management System
Purpose:Detect, display, move and remove duplicate files while maintaining logs and reports.
Author: Komal Mahajan'''

import os
from datetime import datetime
import shutil

class DuplicateFileManager:
    '''
    @Function Name: __init__
    @Description  : This constructor initializes variables required for
                    duplicate file management and log file handling.
    @inputParam   : NONE
    @outParam     : NONE
    @Author       : Komal Mahajan'''
    def __init__(self):
        self.duplicate_files = []
        self.space_saved = 0
        self.log_file = "duplicate_file_logs.txt"

    '''
    @Function Name: write_log
    @Description  : This function stores all system activities into a log file
                    with date and time information.
    @inputParam   : operation (Name of operation performed)
                    details (Operation details)
    @outParam     : NONE
    @Author       : Komal Mahajan'''

    def write_log(self, operation, details):
        try:
            with open(self.log_file, "a") as file:
                file.write("\n")
                file.write("=" * 60 + "\n")
                file.write("Date : {}\n".format(datetime.now()))
                file.write("Operation : {}\n".format(operation))
                file.write(details + "\n")
                file.write("=" * 60 + "\n")

        except Exception as error:
            print("Log Error :", error)



    '''
    @Function Name: scan_folder
    @Description  : This function scans the selected folder and retrieves
                    all files present inside it and its subfolders.
    @inputParam   : folder_path (Path of folder to scan)
    @outParam     : file_list (List containing file paths)
    @Author       : Komal Mahajan'''

    def scan_folder(self, folder_path):
        file_list = []
        try:
            if not os.path.exists(folder_path):
                print("\nFolder does not exist.")
                self.write_log("Folder Scan","Folder not found : {}".format(folder_path) )
                return file_list


            for root, folders, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)



            self.write_log("Folder Scan",
                    "Folder : {}\nTotal Files Found : {}\nStatus : Success".format(folder_path,
                    len(file_list)))

            return file_list

        except Exception as error:
            print("Folder Scan Error :", error)

            self.write_log("Folder Scan","Status : Failed\nReason : {}".format(error))
            return file_list

    '''
    @Function Name: detect_duplicate_files
    @Description  : This function detects duplicate files by comparing file
                    names and file sizes.
    @inputParam   : folder_path (Folder path to scan)
    @outParam     : duplicate_files (List of duplicate files)
    @Author       : Komal Mahajan'''

    def detect_duplicate_files(self, folder_path):
        try:
            self.duplicate_files.clear()
            self.space_saved = 0

            files = self.scan_folder(folder_path)
            unique_files = {}

            for file in files:
                try:
                    file_name = os.path.basename(file)
                    file_size = os.path.getsize(file)

                    key = ( file_name.lower(),file_size)

                except Exception as error:
                    self.write_log( "Duplicate Detection Failed",
                        "File : {}\nReason : {}".format(file, error))

                    continue

                if key in unique_files:
                    duplicate_data = {"file_name": file_name,"original_path": unique_files[key],
                        "duplicate_path": file,"file_size": file_size,"status": "Available"}

                    self.duplicate_files.append(duplicate_data)
                    self.write_log("Duplicate Detected",
                        "File Name : {}\nOriginal : {}\nDuplicate : {}\nSize : {} Bytes".format(file_name,
                            unique_files[key],file,file_size ))

                else:
                    unique_files[key] = file

            print( "\nDuplicate Files Found :",len(self.duplicate_files))

            self.generate_duplicate_report()
            return self.duplicate_files

        except Exception as error:
            print( "Duplicate Detection Error :",  error )
            self.write_log("Duplicate Detection","Status : Failed\nReason : {}".format(error))
            return []

    '''
    @Function Name: display_duplicate_files
    @Description  : This function displays detected duplicate files before
                    performing delete or move operation.
    @inputParam   : NONE
    @outParam     : NONE
    @Author       : Komal Mahajan'''

    def display_duplicate_files(self):
        try:
            if len(self.duplicate_files) == 0:
                print("\nNo Duplicate Files Found.")
                return

            print("\n========== DUPLICATE FILES ==========\n")
            count = 1

            for file in self.duplicate_files:
                print("Duplicate File :", count)
                print("File Name      :", file["file_name"])
                print( "Original Path  :",  file["original_path"] )
                print("Duplicate Path :",file["duplicate_path"])
                print("File Size      :",file["file_size"],"Bytes")
                print("Status         :", file["status"])
                print("-" * 50)

                count += 1

            self.write_log("Display Duplicate Files","Displayed {} duplicate files.".format(
                    len(self.duplicate_files)))

        except Exception as error:
            print( "Display Error :",error)

            self.write_log("Display Duplicate Files","Status : Failed\nReason : {}".format(error))

    '''
    @Function Name: calculate_storage_saved
    @Description  : This function calculates total storage space saved after
                    deleting duplicate files.
    @inputParam   : file_size (Size of deleted duplicate file)
    @outParam     : NONE
    @Author       : Komal Mahajan'''

    def calculate_storage_saved(self, file_size):
        try:
            self.space_saved += file_size

        except Exception as error:
            print("Storage Calculation Error :", error)
            self.write_log("Storage Calculation Failed", str(error))


    '''
    @Function Name: delete_duplicate_files
    @Description  : This function deletes duplicate files permanently after
                    user confirmation and calculates storage saved.
    @inputParam   : NONE
    @outParam     : NONE
    @Author       : Komal Mahajan'''

    def delete_duplicate_files(self):
        try:
            if len(self.duplicate_files) == 0:
                print("\nNo duplicate files available.")
                return

            choice = input("\nDelete duplicate files? (Y/N): ")

            if choice.lower() != "y":
                print("Delete operation cancelled.")
                return

            count = 0

            for file in self.duplicate_files:
                path = file["duplicate_path"]

                if os.path.exists(path):
                    size = os.path.getsize(path)
                    try:
                        os.remove(path)

                    except PermissionError:
                        print("Permission Denied :", path)
                        self.write_log("Delete Failed","Permission Denied : {}".format(path))
                        continue

                    file["status"] = "Deleted"
                    self.calculate_storage_saved(size)

                    count += 1
                    self.write_log("Delete Duplicate File",
                        "File : {}\nSize : {} Bytes\nStatus : Deleted".format(path, size))

            print("\n{} duplicate files deleted.".format(count))
            self.generate_duplicate_report()

        except Exception as error:
            print("Delete Error :", error)
            self.write_log("Delete Operation Failed", str(error))

    '''
    @Function Name: move_duplicate_files
    @Description  : This function moves duplicate files to another folder
                    instead of deleting permanently.
    @inputParam   : destination_folder (Folder path where files are moved)
    @outParam     : NONE
    @Author       : Komal Mahajan'''

    def move_duplicate_files(self, destination_folder):
        try:
            if len(self.duplicate_files) == 0:
                print("\nNo duplicate files available.")
                return

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            count = 0

            for file in self.duplicate_files:
                source = file["duplicate_path"]

                if os.path.exists(source):
                    filename = os.path.basename(source)
                    destination = os.path.join(destination_folder, filename)

                    if os.path.exists(destination):
                        name, extension = os.path.splitext(filename)
                        destination = os.path.join(destination_folder,name + "_copy" + extension)

                    shutil.move(source, destination)
                    file["status"] = "Moved"
                    file["duplicate_path"] = destination
                    count += 1

                    self.write_log("Move Duplicate File",
                        "Source : {}\nDestination : {}\nStatus : Moved".format(source,destination))

            print("\n{} duplicate files moved.".format(count))

        except Exception as error:
            print("Move Error :", error)
            self.write_log("Move Operation Failed", str(error))


    '''
    @Function Name: show_storage_saved
    @Description  : This function displays total storage space saved after
                    deleting duplicate files.
    @inputParam   : NONE
    @outParam     : NONE
    @Author       : Komal Mahajan'''

    def show_storage_saved(self):
        try:
            size = self.space_saved

            if size >= 1024 * 1024:
                print("\nStorage Saved : {:.2f} MB".format(size / (1024 * 1024)))

            elif size >= 1024:
                print("\nStorage Saved : {:.2f} KB".format(size / 1024))

            else:
                print("\nStorage Saved : {} Bytes".format(size))

            self.write_log("Storage Saved","Total Space Saved : {} Bytes".format(size))

        except Exception as error:
            print("Storage Display Error :", error)
            self.write_log("Storage Display Failed", str(error))

    '''
    @Function Name: generate_duplicate_report
    @Description  : This function generates a text report containing duplicate
                    file details.
    @inputParam   : report_file (Report file name)
    @outParam     : NONE
    @Author       : Komal Mahajan'''

    def generate_duplicate_report(self, report_file="duplicate_report.txt"):

        try:
            if len(self.duplicate_files) == 0:
                if os.path.exists(report_file):
                    print("\n========== DUPLICATE FILE REPORT ==========\n")

                    with open(report_file, "r") as file:
                        print(file.read())

                else:
                    print("\nNo duplicate report found.")

                return

            with open(report_file, "a") as file:
                file.write("DUPLICATE FILE REPORT\n")
                file.write("=" * 60 + "\n")
                file.write("Generated Date : {}\n".format(datetime.now()))
                file.write("=" * 60 + "\n\n")

                count = 1

                for data in self.duplicate_files:
                    file.write("Duplicate File : {}\n".format(count))
                    file.write("File Name      : {}\n".format(data["file_name"]))
                    file.write("Original Path  : {}\n".format(data["original_path"]))
                    file.write("Duplicate Path : {}\n".format(data["duplicate_path"]))
                    file.write("File Size      : {} Bytes\n".format(data["file_size"]))
                    file.write("Status         : {}\n".format(data["status"]))
                    file.write("-" * 60 + "\n")

                    count += 1

            print("\nDuplicate report generated successfully.")

            self.write_log("Report Generation",
                "Report File : {}\nStatus : Success".format(report_file))


        except Exception as error:
            print("Report Error :", error)
            self.write_log("Report Generation Failed",str(error))

    '''
    @Function Name: main_menu
    @Description  : This function provides menu options to perform duplicate
                    file management operations.
    @inputParam   : NONE
    @outParam     : NONE
    @Author       : Komal Mahajan
    '''

    def main_menu(self):

        while True:
            print("\n========== DUPLICATE FILE MANAGEMENT ==========")
            print("1. Detect Duplicate Files")
            print("2. Display Duplicate Files")
            print("3. Move Duplicate Files")
            print("4. Delete Duplicate Files")
            print("5. Show Storage Saved")
            print("6. Display  Duplicate Report")
            print("7. Exit")

            choice = input("\nEnter Your Choice : ")

            if choice == "1":
                folder = input("Enter Folder Path : ")
                self.detect_duplicate_files(folder)

            elif choice == "2":
                self.display_duplicate_files()

            elif choice == "3":
                destination = input("Enter Destination Folder : ")
                self.move_duplicate_files(destination)

            elif choice == "4":
                self.delete_duplicate_files()

            elif choice == "5":
                self.show_storage_saved()

            elif choice == "6":
                self.generate_duplicate_report()

            elif choice == "7":
                print("\nProgram Closed.")
                self.write_log("Program Exit","Application closed successfully.")
                break

            else:
                print("\nInvalid Choice.")

# ---------------- MAIN PROGRAM ---------------- #
try:
    manager = DuplicateFileManager()
    manager.main_menu()

except Exception as error:
    print("Program Error :", error)