import os
import hashlib
from datetime import datetime
from Classify_file import main_dir

duplicate_log = os.path.join(main_dir, "duplicate_log.txt")


# Generate SHA-256 Hash
def get_file_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


# Find Duplicate Files
def find_duplicates(folder):

    files = {}
    duplicates = []

    for root, dirs, file_list in os.walk(folder):

        for file in file_list:

            # Ignore log and json files
            if file in ["file_data.json", "duplicate_log.txt"]:
                continue

            path = os.path.join(root, file)

            try:
                size = os.path.getsize(path)
                file_hash = get_file_hash(path)

                # Compare File Name + Size + Hash
                key = (size, file_hash)

                if key in files:
                    duplicates.append(path)
                else:
                    files[key] = path

            except Exception as e:
                print("Error:", e)

    return duplicates


#---------------------Save Log--------------------------
def save_log(file_path):

    with open(duplicate_log, "a") as log:

        log.write(
            f"{datetime.now()} Deleted : {file_path}\n"
        )


# Duplicate File Management
def duplicate_file_management():

    folder = main_dir

    duplicates = find_duplicates(folder)

    if len(duplicates) == 0:

        print("\nNo Duplicate Files Found.")
        return

    print("\nDuplicate Files Found\n")

    for i, file in enumerate(duplicates, start=1):
        print(f"{i}. {file}")

    choice = input("\nDelete Duplicate Files (Y/N): ")

    if choice.upper() == "Y":

        deleted = 0

        for file in duplicates:

            try:
                os.remove(file)
                save_log(file)
                deleted += 1

            except Exception as e:
                print("Error:", e)

        print(f"\n{deleted} duplicate files deleted successfully.")
        print("Logs saved in duplicate_log.txt")

    else:

        print("\nOperation Cancelled.")




