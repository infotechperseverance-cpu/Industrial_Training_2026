from validatation import validate_name
from Classify_file import create_file
from Classify_file import rename_file
from Classify_file import delete_file
from Classify_file import display_records
from Password import password_protection

while True:
    print("===============FILE MANAGEMENT SYSTEM====================")
    print("1. Create File")
    print("2. Rename File")
    print("3. Delete File")
    print("4. Display Records")
    print("5. Exit")
    
    choice=int(input("Enter the Choice:"))

    match choice:
        case 1:
            filename=input("Enter the file name:")

            if validate_name(filename):
               success, password = password_protection()

               if success:
                  create_file(filename)
                  print("File created with password protection.")
               else:
                  create_file(filename)
                  print("File created without password protection.")

        case 2:
            
            old_name = input("Enter the old file name: ")

            new_name = input("Enter the new file name: ")

            rename_file(old_name, new_name)
               
        case 3:
            filename=input("Enter file name which you want to delete")
            delete_file(filename)
        case 4:
            display_records()
        case 5:
            print("Thank you for Using File Management System......!!!!!")
            break
        case _:
            print("Invalid Choice....!! Please try again.")
          