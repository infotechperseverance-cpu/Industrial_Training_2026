
from db_connection import get_connection 
import os  
import shutil
from datetime import datetime
import difflib

'''
@Function Name : add_file
@Description   : This function accepts file details from the user and stores
                 the file information into the Files table. The file path is
                 stored only once so that it can be reused during version
                 management operations.
@Input Param   : file_id (Unique ID of the file)
                 file_path (Complete path of the file)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def add_file():

    file_id = int(input("Enter File ID : "))
    file_path = input("Enter File Path : ")

    if not os.path.exists(file_path):
        print("File Not Found.")
        return
    
    #--Extract only the file name from the file path
    file_name = os.path.basename(file_path)

    try:
        
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO Files(file_id, file_name, file_path)
        VALUES(%s,%s,%s)
        """

        values = (file_id, file_name, file_path)

        cursor.execute(query, values)
        #--Save changes permanently
        connection.commit()
        #--Close database connection
        cursor.close()
        connection.close()

        print("File Added Successfully.")

    except Exception as e:
        print("Error :", e)

'''
@Function Name : get_file_path
@Description   : This function retrieves the original file path from the
                 Files table using the given file ID. The returned path is
                 used by other functions such as create, restore, compare,
                 and delete version.
@Input Param   : file_id (Unique ID of the file)
@Output Param  : file_path (Original file path)
@Author        : Mamata Chaudhari
'''
def get_file_path(file_id):

    try:
        
        connection = get_connection()
        cursor = connection.cursor()
        #--Fetch original file path using File ID
        query = """
        SELECT file_path
        FROM Files
        WHERE file_id = %s
        """

        cursor.execute(query, (file_id,))
        #--Get single record
        result = cursor.fetchone()

        cursor.close()
        connection.close()
        #--Return file path if record exists
        if result:
            return result[0]

        return None  #--file id is not found return none

    except Exception as e:
        print("Error :", e)
        return None


'''
@Function Name : create_version_folder
@Description   : This function checks whether the Versions folder exists.
                 If the folder does not exist, it creates a new folder
                 for storing version files.
@Input Param   : None
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def create_version_folder():

    folder_name = "versions"
    
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print("Version folder created successfully.")

    else:
        print("Version folder already exists.")

'''
@Function Name : create_version
@Description   : This function creates a new version of the selected file.
                 It copies the original file into the Versions folder,
                 generates the next version number, and stores version
                 details in the File_Version table.
@Input Param   : file_id (Unique ID of the file)
                 modified_by (Name of the user)
                 version_notes (Description of the changes)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def create_version():

    file_id = int(input("Enter File ID : "))
    modified_by = input("Modified By : ")
    version_notes = input("Version Notes : ")
    #--Get original file path using File ID
    file_path = get_file_path(file_id)

    if file_path is None:
        print("File ID Not Found.")
        return

    if not os.path.exists(file_path):
        print("Original File Not Found.")
        return

    file_name = os.path.basename(file_path)
    name, extension = os.path.splitext(file_name)
    #--Generate next version number
    version_number = get_latest_version(file_id) + 1

    version_file = f"versions/{name}_v{version_number}{extension}"

    shutil.copy(file_path, version_file)

    try:
        
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO File_Version
        (file_id,file_name,version_number,modified_by,modified_date,version_notes)
        VALUES(%s,%s,%s,%s,%s,%s)
        """

        values = (
            file_id,
            file_name,
            version_number,
            modified_by,
            datetime.now(),
            version_notes
        )
        #--Execute INSERT query
        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        print("Version Created Successfully.")

    except Exception as e:
        print("Database Error :", e)


'''
@Function Name : get_latest_version
@Description   : This function retrieves the latest version number of a
                 file from the File_Version table. If no version exists,
                 it returns 0.
@Input Param   : file_id (Unique ID of the file)
@Output Param  : version_number (Latest version number)
@Author        : Mamata Chaudhari
'''
def get_latest_version(file_id):

    connection = get_connection()
    #--Create cursor object
    cursor = connection.cursor()
    #--Get latest version number for the given file
    query = """
    SELECT MAX(version_number)
    FROM File_Version
    WHERE file_id = %s
    """

    cursor.execute(query, (file_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()
    #--Return 0 if no version exists
    if result[0] is None:
        return 0

    return result[0]


'''
@Function Name : view_version_history
@Description   : This function displays the complete version history of
                 the selected file including version number, modified by,
                 modified date, and version notes.
@Input Param   : file_id (Unique ID of the file)
@Output Param  : Displays version history
@Author        : Mamata Chaudhari
'''
def view_version_history():

    try:
        file_id = int(input("Enter File ID : "))

        connection = get_connection()
        cursor = connection.cursor()
        #--Retrieve version history
        query = """
        SELECT version_number,
               file_name,
               modified_by,
               modified_date,
               version_notes
        FROM File_Version
        WHERE file_id = %s
        ORDER BY version_number
        """

        cursor.execute(query, (file_id,))
        #--Fetch all version records
        records = cursor.fetchall()
    
        if not records:
            print("No Version History Found.")

        else:
            print("\n===== VERSION HISTORY =====\n")

            for row in records:
                print("Version Number :", row[0])
                print("File Name      :", row[1])
                print("Modified By    :", row[2])
                print("Modified Date  :", row[3])
                print("Version Notes  :", row[4])
                print("-" * 40)

        cursor.close()
        connection.close()

    except Exception as e:
        print("Error :", e)


'''
@Function Name : restore_version
@Description   : This function restores the selected version by replacing
                 the current file with the specified version stored in the
                 Versions folder.
@Input Param   : file_id (Unique ID of the file)
                 version_number (Version to be restored)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def restore_version():

    file_id = int(input("Enter File ID : "))
    version_number = int(input("Enter Version Number : "))

    file_path = get_file_path(file_id)
    
    if file_path is None:
        print("File ID Not Found.")
        return
    #--Create version file path
    file_name = os.path.basename(file_path)
    name, extension = os.path.splitext(file_name)

    version_file = f"versions/{name}_v{version_number}{extension}"

    if not os.path.exists(version_file):
        print("Version File Not Found.")
        return
    #--Restore selected version
    shutil.copy(version_file, file_path)

    print("Version Restored Successfully.")

'''
@Function Name : compare_versions
@Description   : This function compares two versions of the same file and
                 displays the line-by-line differences between them using
                 the difflib module.
@Input Param   : file_id (Unique ID of the file)
                 version1 (First version number)
                 version2 (Second version number)
@Output Param  : Displays differences between versions
@Author        : Mamata Chaudhari
'''
def compare_versions():

    file_id = int(input("Enter File ID : "))
    version1 = int(input("Enter First Version Number : "))
    version2 = int(input("Enter Second Version Number : "))

    file_path = get_file_path(file_id)

    if file_path is None:
        print("File ID Not Found.")
        return

    file_name = os.path.basename(file_path)
    name, extension = os.path.splitext(file_name)
    #--Create paths of both version files
    file1 = f"versions/{name}_v{version1}{extension}"
    file2 = f"versions/{name}_v{version2}{extension}"

    binary_extensions = [".pdf", ".docx", ".xlsx", ".jpg", ".jpeg", ".png"]

    if extension.lower() in binary_extensions:
        print("Binary files cannot be compared.")
        return

    if not os.path.exists(file1):  #==Check whether both files exist
        print("First Version File Not Found.")
        return

    if not os.path.exists(file2):
        print("Second Version File Not Found.")
        return

    with open(file1, "r") as f1:
        old_data = f1.readlines()

    with open(file2, "r") as f2:
        new_data = f2.readlines()

    difference = difflib.unified_diff(
        old_data,
        new_data,
        fromfile=file1,
        tofile=file2,
        lineterm=""
    )

    print("\n===== DIFFERENCES =====\n")

    for line in difference:
        print(line)


'''
@Function Name : delete_version
@Description   : This function deletes the selected version file from the
                 Versions folder and removes its corresponding record from
                 the File_Version table.
@Input Param   : file_id (Unique ID of the file)
                 version_number (Version to be deleted)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def delete_version():

    file_id = int(input("Enter File ID : "))
    version_number = int(input("Enter Version Number : "))

    file_path = get_file_path(file_id)

    if file_path is None:
        print("File ID Not Found.")
        return
    # Create version file path
    file_name = os.path.basename(file_path)
    name, extension = os.path.splitext(file_name)

    version_file = f"versions/{name}_v{version_number}{extension}"

    if not os.path.exists(version_file):
        print("Version File Not Found.")
        return
    #--Delete version file
    os.remove(version_file)

    try:

        connection = get_connection()
        cursor = connection.cursor()
        #--Delete version record from database
        query = """
        DELETE FROM File_Version
        WHERE file_id=%s AND version_number=%s
        """

        cursor.execute(query, (file_id, version_number))
        connection.commit()

        cursor.close()
        connection.close()

        print("Version Deleted Successfully.")

    except Exception as e:
        print("Database Error :", e)

'''
@Function Name : main
@Description   : This is the main driver function of the File Version
                 Control module. It creates the Versions folder, displays
                 the menu repeatedly, accepts user choices, and calls the
                 appropriate function based on the selected option.
@Input Param   : None
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def main():
    #--Create Versions folder if it does not exist
    create_version_folder()

    while True:

        print("\n" + "=" * 45)
        print("      FILE VERSION CONTROL")
        print("=" * 45)

        print("1. Add File")
        print("2. Create New Version")
        print("3. View Version History")
        print("4. Restore Version")
        print("5. Compare Versions")
        print("6. Delete Version")
        print("7. Exit")

        choice = input("\nEnter Your Choice : ")

        if choice == "1":
            add_file()

        elif choice == "2":
            create_version()

        elif choice == "3":
            view_version_history()

        elif choice == "4":
            restore_version()

        elif choice == "5":
            compare_versions()

        elif choice == "6":
            delete_version()

        elif choice == "7":
            print("Thank You...")
            break

        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    main()                

                    