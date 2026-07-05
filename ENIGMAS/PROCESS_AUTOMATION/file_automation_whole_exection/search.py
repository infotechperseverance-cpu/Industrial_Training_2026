import os
from fiie_backup import*
def search_file(folder_path, filename):
    """
    Search for a file inside the given folder.
    """

    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    for root, dirs, files in os.walk(folder_path):

        for file in files:

            if file.lower() == filename.lower() :
                Backup_File(file)
                full_path = os.path.join(root, file)

                print("\nFile Found!")
                print("Location:", full_path)

                return

    print("\nFile not found.")
    