import os
import shutil
import logging
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class BackupSystem:
    '''------------------------------------------------------------
    Function Name : __init__
    Description :Initializes Backup System, validates source folder,
                creates backup folder, configures logging,
                establishes MySQL connection and creates database table.
    Author :Komal Mahajan
    ------------------------------------------------------------'''

    def __init__(self, source_folder):
        self.source_folder = os.path.abspath(source_folder)

        if not os.path.exists(self.source_folder):
            raise FileNotFoundError("Source folder does not exist.")

        if not os.path.isdir(self.source_folder):
            raise NotADirectoryError("Invalid source folder.")

        if os.path.basename(self.source_folder).lower() == "backup":
            raise ValueError("Backup folder cannot be selected as source folder.")

        self.backup_folder = os.path.join(self.source_folder,"Backup")
        os.makedirs(self.backup_folder,exist_ok=True)

        logging.basicConfig(filename="backup.log",level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s")

        self.connect_database()
        self.create_database()

    '''------------------------------------------------------------
        Function Name : connect_database
        Description :Connects to MySQL database.
        Author :Komal Mahajan
        ------------------------------------------------------------'''

    def connect_database(self):
        try:
            self.connection = mysql.connector.connect(host="localhost",user="root",password="Youtube@2114",)
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS file_automation")
            self.cursor.execute("USE file_automation")
            self.connection.commit()
            logging.info("Database Connected Successfully.")

        except Error as error:
            logging.error(error)
            raise

    '''------------------------------------------------------------
        Function Name : create_database
        Description :Creates Backup_History table if it does not exist.
        Author :Komal Mahajan
        ------------------------------------------------------------'''

    def create_database(self):
        try:
            query = """
                CREATE TABLE IF NOT EXISTS Backup_History(
                    backup_id INT AUTO_INCREMENT PRIMARY KEY,
                    file_name VARCHAR(255) NOT NULL,category VARCHAR(50) NOT NULL,
                    source VARCHAR(600) NOT NULL,destination VARCHAR(600) NOT NULL,
                    backup_date DATETIME NOT NULL,backup_status VARCHAR(30) NOT NULL)"""

            self.cursor.execute(query)
            self.connection.commit()

            logging.info("Backup_History table created successfully.")

        except Error as error:
            self.connection.rollback()
            logging.error(error)
            raise
        # ===========================================================

    '''
    @Function Name : create_backup_record
    @Description :This function stores backup information into Backup_History table.
    @InputParam :   filename      : Backup File Name
                    category      : File Category
                    source        : Source File Path
                    destination   : Backup Destination Path
                    status        : Backup Status

    @OutParam :NONE
    @Author :Komal Mahajan'''

    def create_backup_record(self,filename,category,source,destination,status):
        try:
            if filename.strip() == "":
                raise ValueError("Invalid File Name.")

            query = """INSERT INTO Backup_History(file_name,category,source,destination,backup_date,
                backup_status ) VALUES (%s,%s,%s,%s,%s,%s)  """

            values = (filename,category,source,destination,datetime.now(),status)

            self.cursor.execute(query,values)
            self.connection.commit()

            logging.info(f"{filename} Record Inserted Successfully.")

        except Error as error:
            self.connection.rollback()
            logging.error(error)

            print("Database Error :",error)

        except Exception as error:
            logging.error(error)
            print(error)

    # ===========================================================

    '''
    @Function Name : display_backup_records
    @Description :Displays complete backup history stored in MySQL database.
    @InputParam :NONE
    @OutParam :NONE
    @Author :Komal Mahajan'''

    def display_backup_records(self):
        try:
            query = """SELECT backup_id, file_name, category,source,destination,backup_date,
                        backup_status FROM Backup_History ORDER BY backup_id DESC """

            self.cursor.execute(query)
            records = self.cursor.fetchall()

            print("\n" + "=" * 170)
            print("BACKUP HISTORY")
            print("=" * 170)

            if len(records) == 0:
                print("No Backup Records Available.")
                return

            print("{:<5} {:<25} {:<12} {:<40} {:<40} {:<22} {:<10}".format("ID",
                    "File Name","Category","Source","Destination","Backup Date","Status" ))
            print("-" * 170)

            for row in records:
                file_name = row[1]
                source = row[3]
                destination = row[4]

                if len(file_name) > 25:
                    file_name = file_name[:22] + "..."

                if len(source) > 40:
                    source = source[:37] + "..."

                if len(destination) > 40:
                    destination = destination[:37] + "..."

                print("{:<5} {:<25} {:<12} {:<40} {:<40} {:<22} {:<10}".format(row[0],
                        file_name,row[2],source,destination,str(row[5]),row[6]))

            print("=" * 170)
            logging.info("Backup History Displayed Successfully.")

        except Error as error:
            logging.error(error)
            print("Unable To Fetch Backup Records.")

        except Exception as error:
            logging.error(error)
            print(error)

    # ===========================================================

    '''
    @Function Name : create_backup
    @Description :Creates backup of a selected file and stores backup information into MySQL database.
    @InputParam :   filepath : Complete File Path
                    category : File Category
    @OutParam :TRUE / FALSE
    @Author :Komal Mahajan'''

    def create_backup(self, filepath, category, show_message=True):
        try:
            filepath = os.path.abspath(filepath)

            if not os.path.exists(filepath):
                print("File does not exist.")
                return False

            if not os.path.isfile(filepath):
                print("Invalid file.")
                return False

            if os.path.getsize(filepath) == 0:
                print("Empty files cannot be backed up.")
                return False

            if filepath.startswith(self.backup_folder):
                print("Cannot backup a file from Backup folder.")
                return False

            if os.path.commonpath([filepath, self.source_folder]) != self.source_folder:
                print("Selected file is outside the source folder.")
                return False

            category = category.strip()

            if category == "":
                category = "General"

            filename = os.path.basename(filepath)
            name, extension = os.path.splitext(filename)
            destination = os.path.join(self.backup_folder,filename)

            counter = 1

            while os.path.exists(destination):
                new_name = (f"{name}_{counter}{extension}")
                destination = os.path.join(self.backup_folder,new_name)
                counter += 1

            shutil.copy2(filepath,destination)
            backup_filename = os.path.basename(destination)
            self.create_backup_record(backup_filename,category,filepath,destination,"SUCCESS")

            logging.info(f"{backup_filename} Backup Created Successfully.")

            if show_message:
                print("\nBackup Created Successfully.")

            return True

        except PermissionError:
            logging.error("Permission Denied.")
            print("Permission Denied.")
            return False

        except Exception as error:
            logging.error(error)

            try:
                self.create_backup_record(os.path.basename(filepath),category,filepath,"",
                                          "FAILED")

            except Exception:
                pass

            print(error)
            return False

    # ===========================================================

    '''
    @Function Name : restore_backup
    @Description :Restores backup file from Backup folder to user selected destination.
    @InputParam :   filename : Backup File Name
                    restore_location : Restore Folder
    @OutParam :TRUE / FALSE
    @Author :Komal Mahajan'''

    def restore_backup(self,filename,restore_location):
        try:
            filename = filename.strip()

            if filename == "":
                print("Invalid file name.")
                return False

            source = os.path.join(self.backup_folder,filename)

            if not os.path.exists(source):
                print("Backup file not found.")
                return False

            restore_location = os.path.abspath(restore_location)
            os.makedirs(restore_location,exist_ok=True)
            destination = os.path.join(restore_location,filename)
            name, extension = os.path.splitext(filename)

            counter = 1

            while os.path.exists(destination):
                destination = os.path.join(restore_location,f"{name}_{counter}{extension}")
                counter += 1

            shutil.copy2(source,destination)
            logging.info(f"{filename} Restored Successfully.")
            print("\nBackup Restored Successfully.")
            return True

        except PermissionError:
            logging.error("Permission Denied.")
            print("Permission Denied.")
            return False

        except Exception as error:
            logging.error(error)
            print(error)
            return False

    # ===========================================================
    '''
    @Function Name : backup_multiple_files
    @Description :This function creates backup of multiple files and displays backup summary.
    @InputParam :   file_list : List of File Paths
                    category  : File Category
    @OutParam :NONE
    @Author :Komal Mahajan'''

    def backup_multiple_files(self, file_list, category):
        success = 0
        failed = 0
        skipped = 0

        try:
            if len(file_list) == 0:
                print("No Files Selected.")
                return

            category = category.strip()

            if category == "":
                category = "General"

            print("\nStarting Multiple File Backup...\n")

            for file in file_list:
                file = file.strip()

                if file == "":
                    skipped += 1
                    continue

                if not os.path.exists(file):
                    print(f"File Not Found : {file}")
                    failed += 1
                    continue

                if self.create_backup(file, category):
                    success += 1

                else:
                    failed += 1

            print("\n" + "=" * 60)
            print("BACKUP SUMMARY")
            print("=" * 60)
            print(f"Total Files       : {len(file_list)}")
            print(f"Successful Backup : {success}")
            print(f"Failed Backup     : {failed}")
            print(f"Skipped Files     : {skipped}")
            print("=" * 60)
            logging.info(f"Multiple Backup Completed | "f"Success={success} "
                f"Failed={failed} "f"Skipped={skipped}")

        except Exception as error:
            logging.error(error)
            print(error)

    # ===========================================================
    '''
    @Function Name : check_backup_status
    @Description :Displays backup status stored in Backup_History table.
    @InputParam :NONE
    @OutParam :NONE
    @Author :Komal Mahajan'''

    def check_backup_status(self):
        try:
            query = """SELECT backup_id,file_name, category,backup_date,backup_status
                        FROM Backup_History ORDER BY backup_date DESC """

            self.cursor.execute(query)
            records = self.cursor.fetchall()

            print("\n" + "=" * 90)
            print("BACKUP STATUS")
            print("=" * 90)

            if len(records) == 0:
                print("No Backup Records Available.")
                return

            print("{:<5} {:<30} {:<12} {:<22} {:<10}".format("ID","File Name","Category",
                    "Backup Date","Status"))
            print("-" * 90)

            success = 0
            failed = 0

            for row in records:
                file_name = row[1]

                if len(file_name) > 30:
                    file_name = file_name[:27] + "..."

                print("{:<5} {:<30} {:<12} {:<22} {:<10}".format(row[0],file_name,row[2],str(row[3]),row[4]))

                if row[4].upper() == "SUCCESS":
                    success += 1

                else:
                    failed += 1

            print("-" * 90)
            print(f"Total Records : {len(records)}")
            print(f"Successful    : {success}")
            print(f"Failed        : {failed}")
            print("=" * 90)
            logging.info("Backup Status Displayed Successfully.")

        except Error as error:
            logging.error(error)
            print("Database Error :", error)

        except Exception as error:
            logging.error(error)
            print(error)

    # ===========================================================
    '''
    @Function Name : delete_old_backups
    @Description :Deletes backup files older than the specified number of days and removes corresponding
                  records from MySQL database.
    @InputParam :days : Number Of Days
    @OutParam :NONE
    @Author :Komal Mahajan'''

    def delete_old_backups(self, days):
        try:
            if not isinstance(days, int):
                print("Invalid Input.")
                return

            if days <= 0:
                print("Days must be greater than zero.")
                return

            if not os.path.exists(self.backup_folder):
                print("Backup Folder Not Found.")
                return

            current_time = datetime.now().timestamp()
            total_files = 0
            deleted_files = 0
            failed_files = 0

            for file in os.listdir(self.backup_folder):
                filepath = os.path.join(self.backup_folder,file)

                if not os.path.isfile(filepath):
                    continue

                total_files += 1
                file_age = (current_time -os.path.getmtime(filepath)) / 86400

                if file_age >= days:
                    try:
                        os.remove(filepath)
                        query = """DELETE FROM Backup_History WHERE destination = %s  """
                        self.cursor.execute(query,(filepath,))
                        self.connection.commit()
                        deleted_files += 1
                        logging.info(f"{file} Deleted Successfully.")

                    except Exception as error:
                        failed_files += 1
                        self.connection.rollback()
                        logging.error(error)

            print("\n" + "=" * 60)
            print("DELETE OLD BACKUP SUMMARY")
            print("=" * 60)
            print(f"Total Backup Files : {total_files}")
            print(f"Deleted Files      : {deleted_files}")
            print(f"Failed Deletions   : {failed_files}")
            print("=" * 60)
            logging.info(f"Delete Old Backup Completed | "f"Deleted={deleted_files}, " f"Failed={failed_files}")

        except Exception as error:
            self.connection.rollback()
            logging.error(error)
            print(error)

    # ===========================================================
    '''
    @Function Name : schedule_backup
    @Description :Creates backup of all files present inside the source folder and its subfolders.
    @InputParam :category : File Category
    @OutParam :NONE
    @Author :Komal Mahajan'''

    def schedule_backup(self, category):
        try:
            category = category.strip()

            if category == "":
                category = "General"

            total_files = 0
            successful = 0
            failed = 0
            skipped = 0

            for root, directories, files in os.walk(self.source_folder):
                if os.path.abspath(root).startswith(self.backup_folder):
                    continue

                for file in files:
                    filepath = os.path.join(root,file)

                    if not os.path.isfile(filepath):
                        skipped += 1
                        continue

                    # Backup only files matching the entered extension
                    if category != "General":
                        if not file.lower().endswith(category.lower()):
                            skipped += 1
                            continue

                    total_files += 1
                    if self.create_backup(filepath,category,show_message=False):
                        successful += 1

                    else:
                        failed += 1

            print("\n" + "=" * 60)
            print("      SCHEDULED BACKUP SUMMARY")
            print("=" * 60)
            print(f"Total Files       : {total_files}")
            print(f"Successful Backup : {successful}")
            print(f"Failed Backup     : {failed}")
            print(f"Skipped Files     : {skipped}")
            print("=" * 60)

            logging.info(f"Scheduled Backup Completed | " f"Total={total_files}, " f"Success={successful}, "
                        f"Failed={failed}, "f"Skipped={skipped}" )

        except Exception as error:
            logging.error(error)
            print(error)

    # ===========================================================
    '''
    @Function Name : show_backup_completed_message
    @Description :Displays backup completion message with system information. 
    @InputParam :NONE
    @OutParam :NONE
    @Author :Komal Mahajan '''

    def show_backup_completed_message(self):
        try:
            print("\n" + "=" * 65)
            print("        BACKUP COMPLETED SUCCESSFULLY")
            print("=" * 65)
            print(f"Source Folder : {self.source_folder}")
            print(f"Backup Folder : {self.backup_folder}")
            print("Database      : file_automation")
            print("Table         : Backup_History")
            print("Log File      : backup.log")
            print("Status        : SUCCESS")
            print("=" * 65)

            logging.info("Backup Completed Successfully." )

        except Exception as error:
            logging.error(error)
            print(error)

    # ===========================================================
    '''
    @Function Name : close_database
    @Description : Safely closes MySQL database connection.
    @InputParam :NONE
    @OutParam :NONE
    @Author :Komal Mahajan '''

    def close_database(self):
        try:
            #hasattr used to check if object has specific attribute
            if hasattr(self, "cursor"):
                self.cursor.close()

            if hasattr(self, "connection"):
                if self.connection.is_connected():
                    self.connection.close()

            logging.info("Database Connection Closed Successfully." )
            print("\nDatabase Connection Closed Successfully.")

        except Error as error:
            logging.error(error)
            print("Database Error :", error)

        except Exception as error:
            logging.error(error)
            print(error)

    # ===========================================================
    '''
    @Function Name : start
    @Description :Displays menu and performs all backup operations.
    @InputParam :NONE
    @OutParam :NONE
    @Author :Komal Mahajan '''

    def start(self):
        while True:
            try:
                print("\n" + "=" * 70)
                print("         AUTOMATIC BACKUP SYSTEM")
                print("=" * 70)
                print("1. Create Backup")
                print("2. Restore Backup")
                print("3. Backup Multiple Files")
                print("4. Display Backup Records")
                print("5. Check Backup Status")
                print("6. Delete Old Backups")
                print("7. Schedule Backup")
                print("8. Exit")

                choice = input("\nEnter Your Choice : ").strip()

                if choice == "1":
                    filepath = input("Enter Complete File Path : ").strip()
                    category = input("Enter File Category : ").strip()

                    if self.create_backup(filepath,category):
                        self.show_backup_completed_message()

                elif choice == "2":
                    filename = input("Enter Backup File Name : ").strip()
                    restore_location = input("Enter Restore Folder Path : ").strip()

                    self.restore_backup(filename,restore_location)

                elif choice == "3":
                    print("\nEnter File Paths (Comma Separated)")
                    file_list = input().split(",")
                    category = input("Enter File Category : ").strip()
                    self.backup_multiple_files(file_list,category)

                elif choice == "4":
                    self.display_backup_records()

                elif choice == "5":
                    self.check_backup_status()

                elif choice == "6":
                    try:
                        days = int(input("Delete Backups Older Than (Days): "))
                        self.delete_old_backups(days)

                    except ValueError:
                        print("Please Enter A Valid Number.")

                elif choice == "7":
                    category = input("Enter File Category : ").strip()
                    self.schedule_backup(category)

                elif choice == "8":
                    self.close_database()
                    print("\nThank You For Using")
                    print("Automatic Backup System")
                    break

                else:
                    print("Invalid Choice. Please Try Again.")

            except KeyboardInterrupt:
                print("\nProgram Interrupted By User.")
                self.close_database()
                break

            except Exception as error:
                logging.error(error)
                print(error)

    # ===========================================================

if __name__ == "__main__":
    print("=" * 70)
    print("      AUTOMATIC BACKUP SYSTEM")
    print("=" * 70)

    try:
        source_folder = input("\nEnter Source Folder Path : ").strip()
        backup = BackupSystem(source_folder)
        backup.start()

    except Exception as error:
        print("\nProgram Terminated.")
        print(error)