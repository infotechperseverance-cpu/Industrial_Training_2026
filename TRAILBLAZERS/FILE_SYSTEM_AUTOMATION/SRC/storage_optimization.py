import os
import hashlib
import shutil
from datetime import datetime
from database import get_connection


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

        inaccessible_files = 0

        try:

            for root, directories, files in os.walk(self.selected_folder):

                for file in files:

                    full_path = os.path.join(root, file)

                    try:

                        if not os.path.isfile(full_path):
                            continue

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

                    except (PermissionError, FileNotFoundError, OSError):

                        inaccessible_files += 1
                        continue

            self.folder_scanned = True

            print(f"\nTotal Files Scanned : {len(self.files)}")

            if inaccessible_files > 0:
                print(f"Inaccessible Files Skipped : {inaccessible_files}")

            self.log_operation(
                operation_type="Folder Scan",
                file_path=self.selected_folder,
                remarks=f"{len(self.files)} files scanned."
            )

        except Exception as error:
            print(f"\nScan Error : {error}")


    def calculate_folder_size(self):

        total_size = 0

        for root, directories, files in os.walk(self.selected_folder):

            for file in files:

                path = os.path.join(root, file)

                try:
                    total_size += os.path.getsize(path)

                except (PermissionError, FileNotFoundError, OSError):
                    continue

        return total_size
    
    def get_unused_days(self, file):

        current_time = datetime.now()

        access_days = (current_time - file["last_access"]).days
        modified_days = (current_time - file["last_modified"]).days

        return max(access_days, modified_days)
    
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
        skipped_files = 0

        print("\nSearching for duplicate files...\n")

        for file in self.files:

            file_hash = self.generate_hash(file["path"])

            if file_hash is None:
                skipped_files += 1
                continue

            if file_hash in file_hashes:

                original = file_hashes[file_hash]

                if original["size"] == file["size"]:

                    duplicate_files.append((original, file))

            else:

                file_hashes[file_hash] = file

        if not duplicate_files:

            print("No duplicate files found.")

            if skipped_files > 0:
                print(f"Skipped Files : {skipped_files}")

            self.log_operation(
                operation_type="Duplicate Scan",
                status="Success",
                remarks="No duplicate files found."
            )

            return

        print("\n" + "=" * 120)
        print(f"{'Original File':<40} {'Duplicate File':<40} {'Size (MB)':>12}")
        print("=" * 120)

        for original, duplicate in duplicate_files:

            size_mb = duplicate["size"] / (1024 * 1024)

            print(f"{original['name'][:40]:<40} {duplicate['name'][:40]:<40} {size_mb:>12.2f}")
            print(f"Original Path  : {original['path']}")
            print(f"Duplicate Path : {duplicate['path']}")
            print("-" * 120)

            self.log_operation(
                operation_type="Duplicate File Found",
                file_name=duplicate["name"],
                file_path=duplicate["path"],
                file_size=duplicate["size"],
                remarks=f"Duplicate of {original['path']}"
            )

        print(f"\nTotal Duplicate Files : {len(duplicate_files)}")

        if skipped_files > 0:
            print(f"Skipped Files : {skipped_files}")

    '''
    @Function Name : identify_large_files

    @Description   : Displays files larger than or equal to the
                    user specified size.

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

            if limit <= 0:
                print("\nSize must be greater than 0.")
                return

            limit_bytes = limit * 1024 * 1024

        except ValueError:

            print("\nInvalid size.")
            return

        large_files = []

        for file in self.files:

            if file["size"] >= limit_bytes:
                large_files.append(file)

        if not large_files:

            print(f"\nNo files larger than or equal to {limit} MB found.")

            self.log_operation(
                operation_type="Large File Scan",
                remarks="No large files found."
            )

            return

        large_files.sort(key=lambda file: file["size"], reverse=True)

        print("\n" + "=" * 120)
        print(f"{'No.':<5} {'File Name':<35} {'Size (MB)':>15} {'Last Modified':>28}")
        print("=" * 120)

        for index, file in enumerate(large_files, start=1):

            size_mb = file["size"] / (1024 * 1024)

            print(f"{index:<5} {file['name'][:35]:<35} {size_mb:>15.2f} {str(file['last_modified']):>28}")
            print(f"Path : {file['path']}")
            print("-" * 120)

            self.log_operation(
                operation_type="Large File Found",
                file_name=file["name"],
                file_path=file["path"],
                file_size=file["size"],
                remarks="Large file detected."
            )

        print(f"\nTotal Large Files : {len(large_files)}")
    
    '''
    @Function Name : generate_hash

    @Description   : Generates SHA-256 hash value for a file.

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

        except (PermissionError, FileNotFoundError, OSError):

            print(f"Unable to access : {file_path}")
            return None

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

    @Description   : Displays files that have not been accessed or
                    modified for the specified number of days.

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

            if days <= 0:
                print("\nDays must be greater than 0.")
                return

        except ValueError:

            print("\nInvalid number.")
            return

        unused_files = []

        for file in self.files:

            unused_days = self.get_unused_days(file)

            if unused_days >= days:
                unused_files.append((file, unused_days))

        if not unused_files:

            print(f"\nNo files unused for more than {days} days.")

            self.log_operation(
                operation_type="Unused File Scan",
                remarks="No unused files found."
            )

            return

        unused_files.sort(key=lambda file: file[1], reverse=True)

        print("\n" + "=" * 120)
        print(f"{'No.':<5} {'File Name':<35} {'Unused Days':>15} {'Size (MB)':>15}")
        print("=" * 120)

        for index, (file, unused_days) in enumerate(unused_files, start=1):

            size_mb = file["size"] / (1024 * 1024)

            print(f"{index:<5} {file['name'][:35]:<35} {unused_days:>15} {size_mb:>15.2f}")
            print(f"Path : {file['path']}")
            print("-" * 120)

            self.log_operation(
                operation_type="Unused File Found",
                file_name=file["name"],
                file_path=file["path"],
                file_size=file["size"],
                remarks=f"Unused for {unused_days} days."
            )

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
            filename = file["name"].lower()

            if extension in self.TEMP_EXTENSIONS or filename.startswith("~") or filename.endswith(".tmp"):

                temporary_files.append(file)

        if not temporary_files:

            print("\nNo temporary files found.")

            self.log_operation(
                operation_type="Temporary File Scan",
                remarks="No temporary files found."
            )

            return

        temporary_files.sort(key=lambda file: file["size"], reverse=True)

        print("\n" + "=" * 120)
        print(f"{'No.':<5} {'File Name':<35} {'Extension':>15} {'Size (MB)':>15}")
        print("=" * 120)

        for index, file in enumerate(temporary_files, start=1):

            extension = os.path.splitext(file["name"])[1]
            size_mb = file["size"] / (1024 * 1024)

            print(f"{index:<5} {file['name'][:35]:<35} {extension:>15} {size_mb:>15.2f}")
            print(f"Path : {file['path']}")
            print("-" * 120)

            self.log_operation(
                operation_type="Temporary File Found",
                file_name=file["name"],
                file_path=file["path"],
                file_size=file["size"],
                remarks="Temporary file detected."
            )

        print(f"\nTotal Temporary Files : {len(temporary_files)}")

    '''
    @Function Name : display_storage_statistics

    @Description   : Displays storage statistics of the selected
                    folder along with drive information.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def display_storage_statistics(self):

        try:

            if self.selected_folder == "":
                self.selected_folder = os.getcwd()

            folder_size = self.calculate_folder_size()

            usage = shutil.disk_usage(self.selected_folder)

            total = usage.total / (1024 ** 3)
            used = usage.used / (1024 ** 3)
            free = usage.free / (1024 ** 3)

            folder_size_mb = folder_size / (1024 ** 2)
            folder_size_gb = folder_size / (1024 ** 3)

            percentage = (folder_size / usage.total) * 100

            print("\n========== Storage Statistics ==========")
            print(f"Selected Folder : {self.selected_folder}")
            print(f"Folder Size     : {folder_size_mb:.2f} MB ({folder_size_gb:.2f} GB)")
            print(f"Drive Capacity  : {total:.2f} GB")
            print(f"Drive Used      : {used:.2f} GB")
            print(f"Drive Free      : {free:.2f} GB")
            print(f"Folder Usage    : {percentage:.4f}% of Drive")
            print("========================================")

            self.log_operation(
                operation_type="Storage Statistics",
                file_path=self.selected_folder,
                remarks="Storage statistics displayed."
            )

        except Exception as error:

            print(f"\nError : {error}")
    '''
    @Function Name : show_free_storage_space

    @Description   : Displays available free storage space for the
                    drive containing the selected folder.

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
            total_space = usage.total / (1024 ** 3)

            folder_size = self.calculate_folder_size() / (1024 ** 3)

            print("\n========== Free Storage Space ==========")
            print(f"Selected Folder : {self.selected_folder}")
            print(f"Folder Size     : {folder_size:.2f} GB")
            print(f"Drive Capacity  : {total_space:.2f} GB")
            print(f"Available Space : {free_space:.2f} GB")
            print("========================================")

            self.log_operation(
                operation_type="Free Storage Check",
                file_path=self.selected_folder,
                remarks=f"{free_space:.2f} GB free."
            )

        except Exception as error:

            print(f"\nError : {error}")

    
    '''
    @Function Name : suggest_files_to_delete

    @Description   : Displays files recommended for deletion based
                    on priority.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def suggest_files_to_delete(self):

        if not self.files:
            self.scan_folder()

        suggestions = []

        for file in self.files:

            extension = os.path.splitext(file["name"])[1].lower()
            unused_days = self.get_unused_days(file)

            priority = 0
            reasons = []

            if extension in self.TEMP_EXTENSIONS:
                priority += 3
                reasons.append("Temporary")

            if file["size"] >= self.LARGE_FILE_SIZE:
                priority += 2
                reasons.append("Large")

            if unused_days >= self.UNUSED_DAYS:
                priority += 1
                reasons.append("Unused")

            if priority > 0:

                suggestions.append({
                    "file": file,
                    "priority": priority,
                    "reason": ", ".join(reasons),
                    "unused_days": unused_days
                })

        if not suggestions:

            print("\nNo files suggested for deletion.")

            self.log_operation(
                operation_type="Deletion Suggestion",
                remarks="No files suggested."
            )
            return

        suggestions.sort(
            key=lambda item: (
                -item["priority"],
                -item["file"]["size"]
            )
        )

        print("\n" + "=" * 120)
        print(f"{'No.':<5} {'File Name':<35} {'Reason':<25} {'Unused Days':>15} {'Size (MB)':>15}")
        print("=" * 120)

        for index, item in enumerate(suggestions, start=1):

            file = item["file"]

            size_mb = file["size"] / (1024 * 1024)

            print(f"{index:<5} {file['name'][:35]:<35} {item['reason']:<25} {item['unused_days']:>15} {size_mb:>15.2f}")
            print(f"Path : {file['path']}")
            print("-" * 120)

        print(f"\nTotal Suggested Files : {len(suggestions)}")

        self.log_operation(
            operation_type="Deletion Suggestion",
            remarks=f"{len(suggestions)} files suggested."
        )
    '''
    @Function Name : delete_file

    @Description   : Deletes the selected file safely after user confirmation.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def delete_file(self):

        if not self.files:
            self.scan_folder()

        path = input("\nEnter complete file path to delete : ").strip()

        if path == "":
            print("\nFile path cannot be empty.")
            return

        if not os.path.exists(path):
            print("\nFile not found.")
            return

        if not os.path.isfile(path):
            print("\nEntered path is not a file.")
            return

        file_name = os.path.basename(path)

        try:
            file_size = os.path.getsize(path)

        except OSError:
            file_size = 0

        print("\nSelected File Details")
        print("-" * 50)
        print(f"File Name : {file_name}")
        print(f"File Size : {file_size / (1024 * 1024):.2f} MB")
        print(f"File Path : {path}")
        print("-" * 50)

        confirm = input("\nType DELETE to permanently delete the file : ").strip().upper()

        if confirm != "DELETE":

            print("\nDeletion cancelled.")

            self.log_operation(
                operation_type="File Deletion Cancelled",
                file_name=file_name,
                file_path=path,
                file_size=file_size,
                status="Cancelled",
                remarks="User cancelled deletion."
            )

            return

        try:

            os.remove(path)

            print("\nFile deleted successfully.")

            self.log_operation(
                operation_type="File Deleted",
                file_name=file_name,
                file_path=path,
                file_size=file_size,
                remarks="Deleted successfully."
            )

            self.scan_folder()

        except PermissionError:

            print("\nFile is currently in use or permission denied.")

            self.log_operation(
                operation_type="File Delete Failed",
                file_name=file_name,
                file_path=path,
                file_size=file_size,
                status="Failed",
                remarks="File is in use or permission denied."
            )

        except FileNotFoundError:

            print("\nFile no longer exists.")

            self.log_operation(
                operation_type="File Delete Failed",
                file_name=file_name,
                file_path=path,
                file_size=file_size,
                status="Failed",
                remarks="File not found."
            )

        except Exception as error:

            print(f"\nDeletion Failed : {error}")

            self.log_operation(
                operation_type="File Delete Failed",
                file_name=file_name,
                file_path=path,
                file_size=file_size,
                status="Failed",
                remarks=str(error)
            )

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


if __name__ == "__main__":

    optimizer = StorageOptimization()

    try:
        optimizer.menu()

    finally:
        optimizer.close_connection()
