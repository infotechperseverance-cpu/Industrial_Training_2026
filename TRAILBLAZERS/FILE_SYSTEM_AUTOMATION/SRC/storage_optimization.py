import os
import hashlib
import shutil
from datetime import datetime
from db_connection import get_connection


class StorageOptimization:

    LARGE_FILE_SIZE = 100 * 1024 * 1024
    UNUSED_DAYS = 30
    TEMP_EXTENSIONS = (".tmp", ".temp", ".log", ".bak", ".cache", ".old")

    '''
    @Function Name : __init__

    @Description   : Initializes database connection, variables
                     and creates required database tables.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()
        self.selected_folder = ""
        self.files = []
        self.folder_scanned = False
        self.create_tables()

    '''
    @Function Name : create_tables

    @Description   : Creates required database tables if they do
                     not already exist.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def create_tables(self):

        try:

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS File_Operations(
                    operation_id INT AUTO_INCREMENT PRIMARY KEY,
                    module_name VARCHAR(100),
                    operation_type VARCHAR(100),
                    file_name VARCHAR(255),
                    file_path TEXT,
                    file_size BIGINT,
                    operation_time DATETIME,
                    status VARCHAR(30),
                    remarks TEXT
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Generated_Reports(
                    report_id INT AUTO_INCREMENT PRIMARY KEY,
                    report_name VARCHAR(150),
                    report_type VARCHAR(50),
                    generated_by VARCHAR(100),
                    generated_date DATETIME,
                    report_status VARCHAR(30)
                )
            """)

            self.connection.commit()

        except Exception as error:
            print(f"\nDatabase Error : {error}")

    '''
    @Function Name : log_operation

    @Description   : Stores operation details into database.

    @InputParam    : operation_type
                     file_name
                     file_path
                     file_size
                     status
                     remarks

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def log_operation(self, operation_type, file_name="", file_path="", file_size=0, status="Success", remarks=""):

        try:

            query = """
                INSERT INTO File_Operations(
                    module_name,
                    operation_type,
                    file_name,
                    file_path,
                    file_size,
                    operation_time,
                    status,
                    remarks
                )
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            """

            values = (
                "Storage Optimization",
                operation_type,
                file_name,
                file_path,
                file_size,
                datetime.now(),
                status,
                remarks
            )

            self.cursor.execute(query, values)
            self.connection.commit()

        except Exception as error:
            print(f"\nLogging Error : {error}")

    '''
    @Function Name : select_folder

    @Description   : Selects folder for storage optimization.

    @InputParam    : NONE

    @OutParam      : True / False

    @Author        : Srushti Subhash Mahajan
    '''

    def select_folder(self):

        folder = input("\nEnter Folder Path : ").strip()

        if folder == "":
            folder = os.getcwd()
            print("\nNo folder entered.")
            print(f"Using Current Directory : {folder}")

        if not os.path.exists(folder):
            print("\nFolder does not exist.")
            return False

        if not os.path.isdir(folder):
            print("\nEntered path is not a folder.")
            return False

        self.selected_folder = folder
        self.folder_scanned = False
        self.log_operation(operation_type="Folder Selected", file_path=folder)

        print("\nFolder Selected Successfully.")
        return True

    '''
    @Function Name : scan_folder

    @Description   : Scans selected folder and stores file details.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def scan_folder(self):

        if self.selected_folder == "":
            self.selected_folder = os.getcwd()
            print("\nNo folder selected.")
            print(f"Scanning Current Directory : {self.selected_folder}")

        elif not self.folder_scanned:
            print("\nSelected folder is not scanned.")
            print(f"Scanning Selected Folder : {self.selected_folder}")
        
        self.files.clear()

        try:

            for root, directories, files in os.walk(self.selected_folder):

                for file in files:

                    full_path = os.path.join(root, file)

                    try:

                        size = os.path.getsize(full_path)
                        accessed_time = datetime.fromtimestamp(os.path.getatime(full_path))
                        modified_time = datetime.fromtimestamp(os.path.getmtime(full_path))

                        self.files.append({
                            "name": file,
                            "path": full_path,
                            "size": size,
                            "last_access": accessed_time,
                            "last_modified": modified_time
                        })

                    except Exception:
                        continue

            print(f"\nTotal Files Scanned : {len(self.files)}")
            self.folder_scanned = True
            self.log_operation(operation_type="Folder Scan", file_path=self.selected_folder, remarks=f"{len(self.files)} files scanned.")

        except Exception as error:
            print(f"\nScan Error : {error}")

    '''
    @Function Name : generate_hash

    @Description   : Generates SHA-256 hash for a file.

    @InputParam    : file_path

    @OutParam      : SHA-256 Hash

    @Author        : Srushti Subhash Mahajan
    '''

    def generate_hash(self, file_path):

        sha256 = hashlib.sha256()

        try:

            with open(file_path, "rb") as file:

                while True:

                    data = file.read(4096)

                    if not data:
                        break

                    sha256.update(data)

            return sha256.hexdigest()

        except Exception:
            return None

    '''
    @Function Name : detect_duplicate_files

    @Description   : Detects duplicate files using SHA-256 hash.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def detect_duplicate_files(self):

        if not self.files:
            self.scan_folder()

        file_hashes = {}
        duplicate_files = []

        print("\nSearching for duplicate files...\n")

        for file in self.files:

            file_hash = self.generate_hash(file["path"])

            if file_hash is None:
                continue

            if file_hash in file_hashes:
                duplicate_files.append((file_hashes[file_hash], file))
            else:
                file_hashes[file_hash] = file

        if not duplicate_files:

            print("No duplicate files found.")

            self.log_operation(operation_type="Duplicate Scan", status="Success", remarks="No duplicate files found.")
            return

        print("\n" + "=" * 120)
        print(f"{'Original File':<58} {'Duplicate File'}")
        print("=" * 120)

        for original, duplicate in duplicate_files:

            print(f"{original['name']:<55} -> {duplicate['name']}")
            print(f"{'Original Path :':<18} {original['path']}")
            print(f"{'Duplicate Path:':<18} {duplicate['path']}")
            print(f"{'Size (MB)     :':<18} {duplicate['size'] / (1024 * 1024):.2f}")
            print("-" * 120)

            self.log_operation(operation_type="Duplicate File Found", file_name=duplicate["name"], file_path=duplicate["path"], file_size=duplicate["size"], remarks=f"Duplicate of {original['path']}")

        print(f"\nTotal Duplicate Files : {len(duplicate_files)}")

    '''
    @Function Name : identify_large_files

    @Description   : Displays files larger than the user-specified
                     size.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def identify_large_files(self):

        if not self.files:
            self.scan_folder()

        try:

            limit = input("\nEnter minimum file size in MB (Default 100): ").strip()

            if limit == "":
                limit = 100

            limit = float(limit)
            limit_bytes = limit * 1024 * 1024

        except ValueError:
            print("\nInvalid size.")
            return

        large_files = []

        for file in self.files:

            if file["size"] >= limit_bytes:
                large_files.append(file)

        if not large_files:

            print(f"\nNo files larger than {limit} MB found.")

            self.log_operation(operation_type="Large File Scan", status="Success", remarks="No large files found.")
            return

        large_files.sort(key=lambda file: file["size"], reverse=True)

        print("\n" + "=" * 120)
        print(f"{'File Name':<35} {'Size (MB)':>12} {'Last Modified':>28}")
        print("=" * 120)

        for file in large_files:

            size_mb = file["size"] / (1024 * 1024)

            print(f"{file['name'][:35]:<35} {size_mb:>12.2f} {str(file['last_modified']):>28}")
            print(f"Path : {file['path']}")
            print("-" * 120)

            self.log_operation(operation_type="Large File Found", file_name=file["name"], file_path=file["path"], file_size=file["size"], remarks="Large file detected.")

        print(f"\nTotal Large Files : {len(large_files)}")

    '''
    @Function Name : display_scanned_files

    @Description   : Displays all scanned files with details.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def display_scanned_files(self):

        if not self.files:
            self.scan_folder()

        if not self.files:
            print("\nNo files available.")
            return

        print("\n" + "=" * 120)
        print(f"{'No.':<5} {'File Name':<35} {'Size (MB)':>12} {'Last Access':>28}")
        print("=" * 120)

        for index, file in enumerate(self.files, start=1):

            size_mb = file["size"] / (1024 * 1024)

            print(f"{index:<5} {file['name'][:35]:<35} {size_mb:>12.2f} {str(file['last_access']):>28}")

        print("=" * 120)
        print(f"Total Files : {len(self.files)}")

    '''
    @Function Name : find_unused_files

    @Description   : Displays files that have not been accessed
                     for the specified number of days.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def find_unused_files(self):

        if not self.files:
            self.scan_folder()

        try:

            days = input("\nEnter unused days (Default 30): ").strip()

            if days == "":
                days = self.UNUSED_DAYS

            days = int(days)

        except ValueError:
            print("\nInvalid number.")
            return

        current_time = datetime.now()
        unused_files = []

        for file in self.files:

            difference = (current_time - file["last_access"]).days

            if difference >= days:
                unused_files.append((file, difference))

        if not unused_files:

            print(f"\nNo files unused for more than {days} days.")

            self.log_operation(operation_type="Unused File Scan", remarks="No unused files found.")
            return

        print("\n" + "=" * 120)
        print(f"{'File Name':<35} {'Unused Days':>15} {'Size (MB)':>15}")
        print("=" * 120)

        for file, difference in unused_files:

            size_mb = file["size"] / (1024 * 1024)

            print(f"{file['name'][:35]:<35} {difference:>15} {size_mb:>15.2f}")
            print(f"Path : {file['path']}")
            print("-" * 120)

            self.log_operation(operation_type="Unused File Found", file_name=file["name"], file_path=file["path"], file_size=file["size"], remarks=f"Unused for {difference} days.")

        print(f"\nTotal Unused Files : {len(unused_files)}")

    '''
    @Function Name : find_temporary_files

    @Description   : Displays temporary files available in the
                     selected folder.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def find_temporary_files(self):

        if not self.files:
            self.scan_folder()

        temporary_files = []

        for file in self.files:

            extension = os.path.splitext(file["name"])[1].lower()

            if extension in self.TEMP_EXTENSIONS:
                temporary_files.append(file)

        if not temporary_files:

            print("\nNo temporary files found.")

            self.log_operation(operation_type="Temporary File Scan", remarks="No temporary files found.")
            return

        print("\n" + "=" * 120)
        print(f"{'File Name':<35} {'Extension':>15} {'Size (MB)':>15}")
        print("=" * 120)

        for file in temporary_files:

            extension = os.path.splitext(file["name"])[1]
            size_mb = file["size"] / (1024 * 1024)

            print(f"{file['name'][:35]:<35} {extension:>15} {size_mb:>15.2f}")
            print(f"Path : {file['path']}")
            print("-" * 120)

            self.log_operation(operation_type="Temporary File Found", file_name=file["name"], file_path=file["path"], file_size=file["size"], remarks="Temporary file detected.")

        print(f"\nTotal Temporary Files : {len(temporary_files)}")

    '''
    @Function Name : display_storage_statistics

    @Description   : Displays storage usage statistics of the
                     selected folder.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def display_storage_statistics(self):

        try:

            if self.selected_folder == "":
                self.selected_folder = os.getcwd()

            usage = shutil.disk_usage(self.selected_folder)

            total = usage.total / (1024 ** 3)
            used = usage.used / (1024 ** 3)
            free = usage.free / (1024 ** 3)
            percentage = (usage.used / usage.total) * 100

            print("\n========== Storage Statistics ==========")
            print(f"Selected Folder : {self.selected_folder}")
            print(f"Total Space     : {total:.2f} GB")
            print(f"Used Space      : {used:.2f} GB")
            print(f"Free Space      : {free:.2f} GB")
            print(f"Usage           : {percentage:.2f}%")
            print("========================================")

            self.log_operation(operation_type="Storage Statistics", file_path=self.selected_folder, remarks="Storage statistics displayed.")

        except Exception as error:
            print(f"\nError : {error}")

    '''
    @Function Name : show_free_storage_space

    @Description   : Displays available free storage space.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def show_free_storage_space(self):

        try:

            if self.selected_folder == "":
                self.selected_folder = os.getcwd()

            usage = shutil.disk_usage(self.selected_folder)

            free_space = usage.free / (1024 ** 3)

            print("\n========== Free Storage Space ==========")
            print(f"Selected Folder : {self.selected_folder}")
            print(f"Available Space : {free_space:.2f} GB")
            print("========================================")

            self.log_operation(operation_type="Free Storage Check", file_path=self.selected_folder, remarks=f"{free_space:.2f} GB free.")

        except Exception as error:
            print(f"\nError : {error}")

    '''
    @Function Name : suggest_files_to_delete

    @Description   : Displays files that are recommended for deletion.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def suggest_files_to_delete(self):

        if not self.files:
            self.scan_folder()

        suggestions = []
        current_time = datetime.now()

        for file in self.files:

            extension = os.path.splitext(file["name"])[1].lower()
            unused_days = (current_time - file["last_access"]).days

            if file["size"] >= self.LARGE_FILE_SIZE or extension in self.TEMP_EXTENSIONS or unused_days >= self.UNUSED_DAYS:
                suggestions.append((file, unused_days))

        if not suggestions:

            print("\nNo files suggested for deletion.")

            self.log_operation(operation_type="Deletion Suggestion", remarks="No files suggested.")
            return

        print("\n" + "=" * 120)
        print(f"{'No.':<5} {'File Name':<35} {'Reason':<20} {'Unused Days':>15} {'Size (MB)':>15}")
        print("=" * 120)

        for index, (file, unused_days) in enumerate(suggestions, start=1):

            extension = os.path.splitext(file["name"])[1].lower()

            if extension in self.TEMP_EXTENSIONS:
                reason = "Temporary File"
            elif file["size"] >= self.LARGE_FILE_SIZE:
                reason = "Large File"
            else:
                reason = "Unused File"

            size_mb = file["size"] / (1024 * 1024)

            print(f"{index:<5} {file['name'][:35]:<35} {reason:<20} {unused_days:>15} {size_mb:>15.2f}")
            print(f"Path : {file['path']}")
            print("-" * 120)

        print(f"\nTotal Suggested Files : {len(suggestions)}")

        self.log_operation(operation_type="Deletion Suggestion", remarks=f"{len(suggestions)} files suggested.")

    '''
    @Function Name : delete_file

    @Description   : Deletes the selected file after user
                     confirmation.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def delete_file(self):

        if not self.files:
            self.scan_folder()

        path = input("\nEnter complete file path to delete : ").strip()

        if not os.path.exists(path):
            print("\nFile not found.")
            return

        confirm = input("Delete this file? (Y/N) : ").strip().upper()

        if confirm != "Y":
            print("\nDeletion cancelled.")
            return
        try:

            file_name = os.path.basename(path)
            file_size = os.path.getsize(path)

            os.remove(path)

            print("\nFile deleted successfully.")

            self.log_operation(operation_type="File Deleted", file_name=file_name, file_path=path, file_size=file_size, remarks="Deleted successfully.")

            self.scan_folder()

        except Exception as error:

            print(f"\nDeletion Failed : {error}")

            self.log_operation(operation_type="File Delete Failed", file_name=os.path.basename(path), file_path=path, status="Failed", remarks=str(error))

    '''
    @Function Name : close_connection

    @Description   : Closes database connection safely.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def close_connection(self):

        try:

            if self.cursor:
                self.cursor.close()

            if self.connection:
                self.connection.close()

        except Exception:
            pass
    '''
    @Function Name : menu

    @Description   : Displays Storage Optimization menu and
                     performs user selected operations.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def menu(self):

        while True:

            print("\n" + "=" * 50)
            print("         STORAGE OPTIMIZATION")
            print("=" * 50)
            print("1. Select Folder")
            print("2. Scan Folder")
            print("3. Display Scanned Files")
            print("4. Detect Duplicate Files")
            print("5. Identify Large Files")
            print("6. Find Unused Files")
            print("7. Find Temporary Files")
            print("8. Display Storage Statistics")
            print("9. Show Free Storage Space")
            print("10. Suggest Files To Delete")
            print("11. Delete File")
            print("12. Exit")
            print("=" * 50)

            choice = input("\nEnter Choice : ").strip()

            if choice == "1":
                self.select_folder()

            elif choice == "2":
                self.scan_folder()

            elif choice == "3":
                self.display_scanned_files()

            elif choice == "4":
                self.detect_duplicate_files()

            elif choice == "5":
                self.identify_large_files()

            elif choice == "6":
                self.find_unused_files()

            elif choice == "7":
                self.find_temporary_files()

            elif choice == "8":
                self.display_storage_statistics()

            elif choice == "9":
                self.show_free_storage_space()

            elif choice == "10":
                self.suggest_files_to_delete()

            elif choice == "11":
                self.delete_file()

            elif choice == "12":

                print("\nThank You For Using Storage Optimization.")

                self.close_connection()

                break

            else:
                print("\nInvalid Choice. Please Enter a Valid Option.")

def close_connection(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close() 

def main():

     obj = StorageOptimization()

     while True:

        print("\n========== STORAGE OPTIMIZATION ==========")
        print("1. Select Folder")
        print("2. Scan Folder")
        print("3. Detect Duplicate Files")
        print("4. Identify Large Files")
        print("5. Find Unused Files")
        print("6. Find Temporary Files")
        print("7. Display Storage Statistics")
        print("8. Show Free Storage Space")
        print("9. Suggest Files To Delete")
        print("10. Delete File")
        print("11. Display Scanned Files")
        print("12. Exit")

        choice = input("Enter Your Choice : ")

        if choice == "1":
            obj.select_folder()

        elif choice == "2":
            obj.scan_folder()

        elif choice == "3":
            obj.detect_duplicate_files()

        elif choice == "4":
            obj.identify_large_files()

        elif choice == "5":
            obj.find_unused_files()

        elif choice == "6":
            obj.find_temporary_files()

        elif choice == "7":
            obj.display_storage_statistics()

        elif choice == "8":
            obj.show_free_storage_space()

        elif choice == "9":
            obj.suggest_files_to_delete()

        elif choice == "10":
            obj.delete_file()

        elif choice == "11":
            obj.display_scanned_files()

        elif choice == "12":
            obj.close_connection()
            break

        else:
            print("Invalid Choice.")


if __name__ == "__main__":
    main()
