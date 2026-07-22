
import pwinput
import os
import json
import csv
import base64
from datetime import datetime
import hashlib
'''
@Function Name : create_files
@Description   : This function creates the required files for the
                 module. It creates a JSON file to store protected
                 file information and a CSV file to store access logs.
@Input Param   : None
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def create_files():

    # Create JSON file if it does not exist
    if not os.path.exists("protected_files.json"):

        with open("protected_files.json", "w") as file:
            json.dump([], file)

    # Create CSV log file if it does not exist
    if not os.path.exists("access_log.csv"):

        with open("access_log.csv","w",newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "File Name",
                "Date",
                "Time",
                "Status"
            ])

    print("Required Files Created Successfully.")

'''
@Function Name : hash_password
@Description   : Generates SHA-256 hash of the password.
@Input Param   : password
@Output Param  : Hashed Password
@Author        : Mamata Chaudhari
'''
def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()    

'''
@Function Name : protect_file
@Description   : This function protects the selected file by
                 accepting a password, saving the file details
                 in JSON format, and encrypting the file content.
@Input Param   : file_path (Path of the file)
                 password (User password)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def protect_file():

    file_path = input("Enter File Path : ").strip()

    if not os.path.exists(file_path):
        print("File Not Found.")
        return

    password = pwinput.pwinput(prompt="Enter Password : ",mask="*").strip()
    
    if password=="":
        print("Password cannot be empty.")
        return

   #--Read saved protected files
    with open("protected_files.json","r") as file:
        data = json.load(file)

    #--Check if file is already protected
    for record in data:

        if record["file_path"] == file_path:

            print("File Already Protected.")
            return

    record = {

        "file_path": file_path,
        "password": hash_password(password)

    }

    data.append(record)

    with open("protected_files.json","w") as file:
        json.dump(
            data,
            file,
            indent=4
        )

    encrypt_file(file_path)

    print("File Protected Successfully.")
    
'''
@Function Name : verify_password
@Description   : This function verifies whether the entered
                 password matches the password stored for the
                 selected protected file.
@Input Param   : file_path (Path of the file)
                 password (User password)
@Output Param  : True or False
@Author        : Mamata Chaudhari
'''
def verify_password(file_path):
    #--read protected file data
    with open("protected_files.json","r") as file:
        data = json.load(file)
    #--Find selected file
    for record in data:
         #--Check entered password
        if record["file_path"] == file_path:

            password = pwinput.pwinput(
                prompt="Enter Password : ",
                mask="*")

            if hash_password(password)==record["password"]: 
                return True

            else:
                print("Incorrect Password")
                return False

    print("File Is Not Protected.")
    return False

'''
@Function Name : save_access_log
@Description   : This function stores file access information
                 such as file name, date, time, and access status
                 in the CSV log file.
@Input Param   : file_name (Name of the file)
                 status (Authorized / Unauthorized)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def save_access_log(file_name, status):
    #--Save file access details in log file
    with open("access_log.csv","a",newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            file_name,
            datetime.now().strftime("%d-%m-%Y"),
            datetime.now().strftime("%H:%M:%S"),
            status
        ])

'''
@Function Name : open_protected_file
@Description   : This function verifies the password before
                 opening a protected file. If the password is
                 correct, the file is decrypted, opened, and
                 access is logged.
@Input Param   : file_path (Path of the file)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def open_protected_file():

    file_path = input("Enter File Path : ").strip()

    if not os.path.exists(file_path):

        print("File Not Found.")
        return
    #--Verify password before opening file
    if verify_password(file_path):

        decrypt_file(file_path)
        #--Save successful access in log
        save_access_log(os.path.basename(file_path),"Authorized")

        os.startfile(file_path)
        input("\nPress enter after closing the file...")

        print("File Opened Successfully.")

    else:
        #--save feaid access in log
        save_access_log(os.path.basename(file_path),"Unauthorized")

'''
@Function Name : view_access_log
@Description   : This function displays the complete access
                 history of protected files from the CSV log file.
@Input Param   : None
@Output Param  : Displays access log
@Author        : Mamata Chaudhari
'''        
def view_access_log():

    try:

        with open("access_log.csv","r") as file:

            reader = csv.reader(file)

            print("\n===== ACCESS LOG =====\n")

            for row in reader:

                print(row)

    except Exception as e:
        print("Error :",e)

'''
@Function Name : change_password
@Description   : This function allows the user to change the
                 password of a protected file after verifying
                 the current password.
@Input Param   : file_path (Path of the file)
                 old_password (Current password)
                 new_password (New password)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def change_password():

    file_path = input("Enter File Path : ").strip()

    if not os.path.exists(file_path):

        print("File Not Found.")

        return

    with open("protected_files.json","r") as file:
        data = json.load(file)

    for record in data:

        #--Find matching protected file
        if record["file_path"] == file_path:

            old_password = pwinput.pwinput(
               prompt="Enter Current Password : ",
               mask="*"
            )
        
             #--Verify current password
            if hash_password(old_password)!=record["password"]: 

                print("Incorrect Password.")
                return

            new_password = pwinput.pwinput(
                prompt="Enter New Password : ",
                mask="*"
            )
            new_password = new_password.strip()
            if new_password == "":
             print("New Password cannot be empty.")
             return
            #--Update password
            record["password"] = hash_password(new_password)

            with open("protected_files.json","w") as file:
                json.dump(
                    data,
                    file,
                    indent=4
                )

            print("Password Changed Successfully.")
            return

    print("File Is Not Protected.")

'''
@Function Name : remove_password
@Description   : This function removes password protection from
                 a protected file after verifying the current
                 password. It also decrypts the file before
                 removing protection.
@Input Param   : file_path (Path of the file)
                 password (Current password)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def remove_password():

    file_path = input("Enter File Path : ").strip()

    if not os.path.exists(file_path):

        print("File Not Found.")
        return

    with open("protected_files.json","r") as file:
        data = json.load(file)

    for record in data:

        if record["file_path"] == file_path:

            password = pwinput.pwinput(
                 prompt="Enter Current Password : ",
                 mask="*"
            )
            #--Verify password
            if hash_password(password)!=record["password"]:

                print("Incorrect Password.")
                return

            #--Decrypt file before removing protection
            decrypt_file(file_path)

            data.remove(record)

            with open("protected_files.json","w") as file:
                json.dump(
                    data,
                    file,
                    indent=4
                )

            print("Password Removed Successfully.")
            return

    print("File Is Not Protected.")

'''
@Function Name : encrypt_file
@Description   : This function encrypts the selected file by
                 converting its content into encoded format for
                 enhanced security.
@Input Param   : file_path (Path of the file)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def encrypt_file(file_path):

    try:

        with open(file_path,"rb") as file:
            data = file.read()

        try:
            base64.b64decode(data,validate=True)
            print("File is already encrypted.")
            return
        except:
            pass    
        #--Convert data into encrypted format
        encrypted_data = base64.b64encode(data)
        #--save data in file 
        with open(file_path,"wb") as file:

            file.write(encrypted_data)

        print("File Encrypted Successfully.")

    except Exception as e:
        print("Error :",e)

'''
@Function Name : decrypt_file
@Description   : This function decrypts the encrypted file and
                 converts the encoded content back into its
                 original readable format.
@Input Param   : file_path (Path of the file)
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def decrypt_file(file_path):

    try:

        with open(file_path,"rb") as file:
            encrypted_data = file.read()

        encrypted_data += b'='*(-len(encrypted_data)%4)    
        #--Convert data back to original format
        original_data = base64.b64decode(encrypted_data)
        #--save data in file 
        with open(file_path,"wb") as file:
            file.write(original_data)

        print("File Decrypted Successfully.")

    except Exception as e:
        print("Error :",e)            

'''
@Function Name : main
@Description   : This is the main driver function of the File
                 Password Protection module. It displays the
                 menu, accepts user choices, and calls the
                 appropriate function based on the selected option.
@Input Param   : None
@Output Param  : None
@Author        : Mamata Chaudhari
'''
def main():

    create_files()

    while True:

        print("\n" + "=" * 40)
        print("    FILE PASSWORD PROTECTION")
        print("=" * 40)

        print("1. Protect File")
        print("2. Open Protected File")
        print("3. Change Password")
        print("4. Remove Password")
        print("5. View Access Log")
        print("6. Exit")

        choice = input("\nEnter Your Choice : ")

        if choice == "1":
            protect_file()

        elif choice == "2":
            open_protected_file()

        elif choice == "3":
            change_password()

        elif choice == "4":
            remove_password()

        elif choice == "5":
            view_access_log()

        elif choice == "6":
            print("Thank You...")
            break

        else:
            print("Invalid Choice! Please Try Again.")


if __name__ == "__main__":

    main()        
