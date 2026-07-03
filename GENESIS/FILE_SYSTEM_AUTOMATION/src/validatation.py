import os
import re

main_dir = "File_Manager"

def validate_name(filename):

    invalid_char = r'[\\/:*?"<>|]'

    if filename.strip() == "":
        print("Filename cannot be empty.")
        return False

    elif re.search(invalid_char, filename):
        print("Filename contains invalid characters.")
        return False

    elif len(filename) > 50:
        print("Filename is too long.")
        return False

    # Check if file already exists in File_Manager
    for root, dirs, files in os.walk(main_dir):
        if filename in files:
            print("File already exists.")
            return False

    return True