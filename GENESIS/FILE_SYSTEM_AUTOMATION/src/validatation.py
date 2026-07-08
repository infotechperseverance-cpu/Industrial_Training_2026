import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.join(BASE_DIR, "File_Manager")

def validate_name(filename):
    invalid_char = r'[\\/:*?"<>|]'

    if filename.strip() == "":
        print("Filename cannot be empty.")
        return False

    elif re.search(invalid_char, filename):
        print("Filename contains invalid characters (\\ / : * ? \" < > |).")
        return False

    elif len(filename) > 50:
        print("Filename is too long (Max 50 characters).")
        return False

    from Classify_file import classification_file, load_data
    records = load_data()
    for item in records:
        if item["filename"].lower() == filename.lower():
            print("File already exists in database.")
            return False

    category = classification_file(filename)
    specific_folder = os.path.join(main_dir, category)
    full_path = os.path.join(specific_folder, filename)

    if os.path.exists(full_path):
        print(f"File already exists physically in '{category}' folder.")
        return False

    return True