import os
import difflib
from datetime import datetime
from database import get_connection


class SmartFileSearch:

    '''
    @Function Name: __init__
    @Description  : This function initializes database connection and active folder details.
    @inputParam   : NONE
    @outParam    : NONE
    @Author       : Srushti Mahajan
    '''
    def __init__(self):

        # Establish database connection
        self.connection = get_connection()

        # Store selected folder path
        self.scanned_folder = None


    '''
    @Function Name: create_table
    @Description  : This function creates Files table in database if it does not exist.
    @inputParam   : NONE
    @outParam    : NONE
    @Author       : Srushti Mahajan
    '''
    def create_table(self):

        # SQL query for creating Files table
        query = """
        CREATE TABLE IF NOT EXISTS Files(
            file_id INT AUTO_INCREMENT PRIMARY KEY,
            file_name VARCHAR(255),
            file_path TEXT,
            file_type VARCHAR(50),
            file_size BIGINT,
            created_date DATETIME
        )
        """

        # Create cursor object
        cursor = self.connection.cursor()

        # Execute table creation query
        cursor.execute(query)

        # Save changes
        self.connection.commit()


    '''
    @Function Name: file_exists
    @Description  : This function checks whether file path already exists in database.
    @inputParam   : path(file path)
    @outParam    : Returns existing file record or None
    @Author       : Srushti Mahajan
    '''
    def file_exists(self, path):

        # Create cursor object
        cursor = self.connection.cursor()

        # Query to check duplicate file
        query = """
        SELECT file_id FROM Files WHERE file_path=%s
        """

        # Execute duplicate check
        cursor.execute(query, (path,))

        # Return matching record
        return cursor.fetchone()


    '''
    @Function Name: format_date
    @Description  : This function converts datetime into required display format.
    @inputParam   : date(datetime value)
    @outParam    : Returns formatted date string
    @Author       : Srushti Mahajan
    '''
    def format_date(self, date):

        # Convert date into readable format
        return date.strftime("%d-%m-%Y %H:%M:%S")


    '''
    @Function Name: display_file_details
    @Description  : This function displays details of files received from database.
    @inputParam   : rows(file records)
    @outParam    : NONE
    @Author       : Srushti Mahajan
    '''
    def display_file_details(self, rows):

        # Display each file record
        for row in rows:

            print("\n================================")
            print("File Name :", row["file_name"])
            print("Path      :", row["file_path"])
            print("Type      :", row["file_type"])
            print("Size      :", row["file_size"], "bytes")
            print("Created   :", self.format_date(row["created_date"]))

        print("================================")


    '''
    @Function Name: scan_folder
    @Description  : This function scans selected folder and stores file details into database.
    @inputParam   : folder(folder path)
    @outParam    : NONE
    @Author       : Srushti Mahajan
    '''
    def scan_folder(self, folder):

        # Check folder existence
        if not os.path.exists(folder):
            print("Invalid folder path.")
            return

        # Store absolute folder path
        self.scanned_folder = os.path.abspath(folder)

        # Create cursor object
        cursor = self.connection.cursor()

        # Traverse folder and subfolders
        for root, dirs, files in os.walk(self.scanned_folder):

            # Process every file
            for file in files:

                # Create complete file path
                full_path = os.path.abspath(os.path.join(root, file))

                # Skip duplicate files
                if self.file_exists(full_path):
                    continue

                # Get file information
                extension = os.path.splitext(file)[1]
                size = os.path.getsize(full_path)
                created = datetime.fromtimestamp(os.path.getctime(full_path))

                # Insert file details query
                query = """
                INSERT INTO Files(file_name,file_path,file_type,file_size,created_date)
                VALUES(%s,%s,%s,%s,%s)
                """

                # Insert file data
                cursor.execute(query, (file, full_path, extension, size, created))

        # Save database changes
        self.connection.commit()

        print("Folder scanned successfully.")

    '''
        @Function Name: ensure_folder_selected
        @Description  : This function checks whether folder is selected. If not, it scans current   directory.
        @inputParam   : NONE
        @outParam    : NONE
        @Author       : Srushti Mahajan
    '''
    def ensure_folder_selected(self):

        # Check if folder is selected
        if self.scanned_folder is None:

            print("No folder selected.")
            print("System will perform operations on current directory.")

            # Scan current working directory
            self.scan_folder(os.getcwd())


    '''
    @Function Name: get_active_files
    @Description  : This function retrieves files from currently active folder.
    @inputParam   : NONE
    @outParam    : Returns list of active folder files
    @Author       : Srushti Mahajan
    '''
    def get_active_files(self):

        # Ensure folder availability
        self.ensure_folder_selected()

        # Create database cursor
        cursor = self.connection.cursor()

        # Fetch all files
        cursor.execute("SELECT * FROM Files")

        all_files = cursor.fetchall()

        active_files = []

        # Get active folder path
        active_folder = os.path.abspath(self.scanned_folder)

        # Filter files belonging to active folder
        for file in all_files:

            stored_path = os.path.abspath(file["file_path"])

            if stored_path.startswith(active_folder):
                active_files.append(file)

        return active_files


    '''
    @Function Name: search_by_name
    @Description  : This function searches files using file name and provides suggestions for similar names.
    @inputParam   : name(file name to search)
    @outParam    : NONE
    @Author       : Srushti Mahajan
    '''
    def search_by_name(self, name):

        # Get files from active folder
        files = self.get_active_files()

        result = []

        # Compare file names
        for file in files:

            if name.lower() in file["file_name"].lower():
                result.append(file)

        # Display matching files
        if result:

            print("Matching Files:")
            self.display_file_details(result)

        else:

            print("No file found.")

            file_names = []

            # Store all file names
            for file in files:
                file_names.append(file["file_name"])

            # Find similar names
            suggestions = difflib.get_close_matches(name, file_names, n=3, cutoff=0.5)

            if suggestions:

                print("Did you mean:")

                for item in suggestions:
                    print("-", item)

            else:
                print("No similar file found.")


    '''
    @Function Name: search_by_extension
    @Description  : This function searches files based on their extension type.
    @inputParam   : extension(file extension)
    @outParam    : NONE
    @Author       : Srushti Mahajan
    '''
    def search_by_extension(self, extension):

        # Get active folder files
        files = self.get_active_files()

        result = []

        # Compare file extensions
        for file in files:

            if file["file_type"].lower() == extension.lower():
                result.append(file)

        # Display search result
        if result:
            self.display_file_details(result)

        else:
            print("No files found.")


    '''
    @Function Name: search_by_size
    @Description  : This function searches files based on maximum file size.
    @inputParam   : size(maximum file size in bytes)
    @outParam    : NONE
    @Author       : Srushti Mahajan
    '''
    def search_by_size(self, size):

        # Get active folder files
        files = self.get_active_files()

        result = []

        # Compare file sizes
        for file in files:

            if file["file_size"] <= size:
                result.append(file)

        # Display search result
        if result:
            self.display_file_details(result)

        else:
            print("No files found.")


    '''
    @Function Name: search_by_date
    @Description  : This function searches files based on file creation date.
    @inputParam   : date(file creation date)
    @outParam    : NONE
    @Author       : Srushti Mahajan
    '''
    def search_by_date(self, date):

        # Get active folder files
        files = self.get_active_files()

        result = []

        # Compare file creation date
        for file in files:

            file_date = file["created_date"].strftime("%Y-%m-%d")

            if file_date == date:
                result.append(file)

        # Display search result
        if result:
            self.display_file_details(result)

        else:
            print("No files found.")

    '''
        @Function Name: display_all
        @Description  : This function displays all files available in selected folder.
        @inputParam   : NONE
        @outParam    : NONE
        @Author       : Srushti Mahajan
    '''
    def display_all(self):

        # Get files from active folder
        files = self.get_active_files()

        # Display available files
        if files:

            print("Files in selected folder:")
            self.display_file_details(files)

        else:

            print("No files found in selected folder.")


    '''
    @Function Name: close
    @Description  : This function closes database connection.
    @inputParam   : NONE
    @outParam    : NONE
    @Author       : Srushti Mahajan
    '''
    def close(self):

        # Check database connection
        if self.connection:

            # Close connection
            self.connection.close()

            print("Database connection closed.")



# ---------------------------------
# Standalone Execution
# ---------------------------------

if __name__ == "__main__":

    # Create SmartFileSearch object
    obj = SmartFileSearch()

    # Create database table
    obj.create_table()

    while True:

        print("\n========== Smart File Search ==========")
        print("1. Scan Folder")
        print("2. Search By Name")
        print("3. Search By Extension")
        print("4. Search By Size")
        print("5. Search By Date")
        print("6. Display All Files")
        print("7. Exit")

        # Accept user choice
        choice = input("Enter your choice: ")

        try:

            # Scan folder option
            if choice == "1":

                folder = input("Enter Folder Path: ")
                obj.scan_folder(folder)


            # Search by name option
            elif choice == "2":

                name = input("Enter File Name: ")
                obj.search_by_name(name)


            # Search by extension option
            elif choice == "3":

                extension = input("Enter Extension (Example .py): ")
                obj.search_by_extension(extension)


            # Search by size option
            elif choice == "4":

                size = int(input("Enter maximum size in bytes: "))
                obj.search_by_size(size)


            # Search by date option
            elif choice == "5":

                date = input("Enter Date (YYYY-MM-DD): ")
                obj.search_by_date(date)


            # Display all files option
            elif choice == "6":

                obj.display_all()


            # Exit program
            elif choice == "7":

                obj.close()

                print("Program Closed.")

                break


            else:

                print("Invalid Choice.")


        except ValueError:

            # Handle invalid numeric input
            print("Please enter valid input.")


        except Exception as e:

            # Handle unexpected errors
            print("Error:", e)