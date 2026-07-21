import os
import shutil
from datetime import datetime
from db_connection import get_connection

'''
@Function Name : delete_file
@Description   : This function deletes a file from its original location,
                 saves a backup copy, moves the file to the Recycle Folder,
                 and stores file details in the database.
@Input Param   : File Path
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def delete_file():

    file_path = input("Enter File Path : ").strip()

    if not os.path.exists(file_path):
        print("File Not Found.")
        return

    file_name = os.path.basename(file_path)

    #--Create Backup Folder
    backup_folder = "Backup_Folder"

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    backup_path = os.path.join(backup_folder,file_name)

    #--Save backup copy
    shutil.copy2(file_path,backup_path)

    #--Create Recycle Folder
    recycle_folder = "Recycle_Folder"

    if not os.path.exists(recycle_folder):

        os.makedirs(recycle_folder)

    recycle_path = os.path.join(recycle_folder,file_name)

    #--Move file to recycle folder
    shutil.move(file_path,recycle_path)

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO Recycle_Bin
    (
        file_id,
        file_name,
        deleted_date,
        recovery_status,
        deleted_by
    )
    VALUES (%s,%s,%s,%s,%s)
    """

    values = (
        None,
        file_name,
        datetime.now().date(),
        "Deleted",
        os.getlogin()
    )

    cursor.execute(query,values)

    connection.commit()
    connection.close()

    print("File Moved To Recycle Bin Successfully.")

'''
@Function Name : show_deleted_files
@Description   : This function displays all deleted files stored
                 in the Recycle Bin table.
@Input Param   : None
@Output Param  : List of Deleted Files
@Author        : Mamata Chaudhari
'''    
def show_deleted_files():

    connection = get_connection()
    cursor = connection.cursor()
      #--Get deleted file details from database
    query = """
    SELECT
    recovery_id,
    file_name,
    deleted_date,
    recovery_status
    FROM Recycle_Bin
    """

    cursor.execute(query)
    records = cursor.fetchall()
    
    if len(records) == 0:
        print("No Deleted Files Found.")

    else:
        print("\n===== DELETED FILES =====\n")
        for record in records:

            print("Recovery ID :",record[0])

            print("File Name   :",record[1])

            print("Deleted Date:",record[2])

            print("Status      :",record[3])

            print("-" * 30)

    connection.close()

'''
@Function Name : preview_file
@Description   : This function displays complete details of a
                 selected deleted file using Recovery ID.
@Input Param   : Recovery ID
@Output Param  : File Details
@Author        : Mamata Chaudhari
'''
def preview_file():

    recovery_id = input("Enter Recovery ID : ")

    connection = get_connection()
    cursor = connection.cursor()
     #--Get file details using Recovery ID
    query = """
    SELECT *
    FROM Recycle_Bin
    WHERE recovery_id = %s
    """

    cursor.execute(query,(recovery_id,))
    record = cursor.fetchone()

    if record is None:
        print("File Not Found.")

    else:
        print("\n===== FILE PREVIEW =====\n")
        print("Recovery ID    :",record[0])
        print("File ID        :",record[1])
        print("File Name      :",record[2])
        print("Deleted Date   :",record[3])
        print("Recovered Date :",record[4])
        print("Recovery Status:",record[5])
        print("Deleted By     :",record[6])

    connection.close()

'''
@Function Name : recover_file
@Description   : This function recovers a deleted file from the
                 Recycle Folder and updates the recovery status.
@Input Param   : Recovery ID
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def recover_file():

    recovery_id = input("Enter Recovery ID : ")

    connection = get_connection()
    cursor = connection.cursor()
    #--Get deleted file name using Recovery ID
    query = """
    SELECT
    file_name
    FROM Recycle_Bin
    WHERE recovery_id = %s
    AND recovery_status = 'Deleted'
    """

    cursor.execute(query,(recovery_id,))
    record = cursor.fetchone()

    if record is None:

        print("File Not Found.")
        connection.close()
        return

    file_name = record[0]

    recycle_path = os.path.join("Recycle_Folder",file_name)

    recovery_folder = "Recovered_Files"
     #--Create recovery folder if it does not exist
    if not os.path.exists(recovery_folder):

        os.makedirs(recovery_folder)

    recovered_path = os.path.join(recovery_folder,file_name)

    if not os.path.exists(recycle_path):

        print(file_name,"Not Found In Recycle Folder.")

        connection.close()
        return
    #--Move file to Recovered Files folder
    shutil.move(recycle_path,recovered_path)
    #--Update recovery details in database
    update_query = """
    UPDATE Recycle_Bin
    SET recovered_date = %s,
        recovery_status = %s
    WHERE recovery_id = %s
    """

    cursor.execute(
        update_query,
        (
            datetime.now().date(),
            "Recovered",
            recovery_id
        )
    )

    connection.commit()
    connection.close()

    print("File Recovered Successfully.")

'''
@Function Name : recover_multiple_files
@Description   : This function recovers multiple deleted files
                 using Recovery IDs entered by the user.
@Input Param   : Recovery IDs
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def recover_multiple_files():

    recovery_ids = input("Enter Recovery IDs (Comma Separated) : ")

    recovery_ids = recovery_ids.split(",")

    connection = get_connection()
    cursor = connection.cursor()

    recovered_count = 0
    #--Process each Recovery ID
    for recovery_id in recovery_ids:

        recovery_id = recovery_id.strip()
         #--Get file name using Recovery ID
        query = """
        SELECT file_name
        FROM Recycle_Bin
        WHERE recovery_id = %s
        AND recovery_status = 'Deleted'
        """

        cursor.execute(query,(recovery_id,))

        record = cursor.fetchone()

        if record is None:

            print("Recovery ID",recovery_id,"Not Found.")
            continue

        file_name = record[0]

        recycle_path = os.path.join("Recycle_Folder",file_name)

        recovery_folder = "Recovered_Files"

        if not os.path.exists(recovery_folder):

            os.makedirs(recovery_folder)

        recovered_path = os.path.join(recovery_folder,file_name)

        if not os.path.exists(recycle_path):

            print(file_name,"Not Found In Recycle Folder.")
            continue

        shutil.move(recycle_path,recovered_path)

        update_query = """
        UPDATE Recycle_Bin
        SET recovered_date = %s,
            recovery_status = %s
        WHERE recovery_id = %s
        """

        cursor.execute(
            update_query,
            (
                datetime.now().date(),
                "Recovered",
                recovery_id
            )
        )

        recovered_count += 1

    connection.commit()
    connection.close()

    print(recovered_count,"Files Recovered Successfully.")

'''
@Function Name : restore_backup
@Description   : This function restores a file from the
                 Backup Folder to the Recovered Files Folder.
@Input Param   : File Name
@Output Param  : None
@Author        : Mamata Chaudhari
'''    
def restore_backup():

    file_name = input("Enter File Name : ").strip()

    backup_folder = "Backup_Folder"

    backup_file = os.path.join(backup_folder,file_name)

    if not os.path.exists(backup_file):
        print("Backup File Not Found.")
        return

    restore_folder = ("Recovered_Files")

    if not os.path.exists(restore_folder):
        os.makedirs(restore_folder)

    restore_path = os.path.join(restore_folder,file_name)
    #--Copy file from Backup Folder to Recovered Files
    shutil.copy2(backup_file,restore_path)

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE Recycle_Bin
    SET recovered_date = %s,
        recovery_status = %s
    WHERE file_name = %s
    """

    cursor.execute(
        query,
        (
            datetime.now().date(),
            "Backup Restored",
            file_name
        )
    )

    connection.commit()
    connection.close()

    print("Backup Restored Successfully.")

'''
@Function Name : permanent_delete
@Description   : This function permanently deletes a file from
                 the Recycle Folder and removes its database record.
@Input Param   : Recovery ID
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def permanent_delete():

    recovery_id = input("Enter Recovery ID : ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT file_name
    FROM Recycle_Bin
    WHERE recovery_id = %s
    """

    cursor.execute(query,(recovery_id,))
    record = cursor.fetchone()

    if record is None:
        print("File Not Found.")
        connection.close()
        return

    file_name = record[0]

    recycle_path = os.path.join("Recycle_Folder",file_name)
    #--Delete file from Recycle Folder
    if os.path.exists(recycle_path):
        os.remove(recycle_path)

    delete_query = """
    DELETE FROM Recycle_Bin
    WHERE recovery_id = %s
    """

    cursor.execute(delete_query,(recovery_id,))

    connection.commit()
    connection.close()

    print("File Permanently Deleted.")

'''
@Function Name : show_recovery_status
@Description   : This function displays the recovery status
                 of all files stored in the database.
@Input Param   : None
@Output Param  : Recovery Details
@Author        : Mamata Chaudhari
'''
def show_recovery_status():

    connection = get_connection()
    cursor = connection.cursor()
    #--Get recovery details from database
    query = """
    SELECT
    recovery_id,
    file_name,
    deleted_date,
    recovered_date,
    recovery_status
    FROM Recycle_Bin
    """

    cursor.execute(query)
    records = cursor.fetchall()
    #--Check if recovery records exist
    if len(records) == 0:
        print("No Recovery Records Found.")

    else:
        print("\n===== RECOVERY STATUS =====\n")

        for record in records:

            print("Recovery ID    :",record[0])
            print("File Name      :",record[1])
            print("Deleted Date   :",record[2])
            print("Recovered Date :",record[3])
            print("Status         :",record[4])
            print("-" * 40)

    connection.close()

'''
@Function Name : create_folders
@Description   : This function creates the required folders
                 for file recovery operations if they do not exist.
@Input Param   : None
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def create_folders():

    if not os.path.exists("Recycle_Folder"):
        os.makedirs("Recycle_Folder")

    if not os.path.exists("Recovered_Files"):
        os.makedirs("Recovered_Files")

    if not os.path.exists("Backup_Folder"):
        os.makedirs("Backup_Folder")

'''
@Function Name : main
@Description   : This function displays the menu and calls
                 the appropriate function based on user choice.
@Input Param   : User Choice
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def main():

    create_folders()

    while True:

        print("\n" + "=" * 40)
        print("      FILE RECOVERY SYSTEM")
        print("=" * 40)

        print("1. Delete File")
        print("2. Show Deleted Files")
        print("3. Preview File")
        print("4. Recover File")
        print("5. Recover Multiple Files")
        print("6. Restore Backup")
        print("7. Permanent Delete")
        print("8. Show Recovery Status")
        print("9. Exit")

        choice = input("\nEnter Your Choice : ")

        if choice == "1":
            delete_file()

        elif choice == "2":
            show_deleted_files()

        elif choice == "3":
            preview_file()

        elif choice == "4":
            recover_file()

        elif choice == "5":
            recover_multiple_files()

        elif choice == "6":
            restore_backup()

        elif choice == "7":
            permanent_delete()

        elif choice == "8":
            show_recovery_status()

        elif choice == "9":
            print("Thank You...")
            break

        else:
            print("Invalid Choice! Please Try Again.")

if __name__ == "__main__":

    main()