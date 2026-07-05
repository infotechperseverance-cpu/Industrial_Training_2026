#File Renaming
import os
from write_log import write_log
from fiie_backup import *
def rename_duplicates(folder_path):

    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    file_count = {}

    files = os.listdir(folder_path)

    for file in files:

        old_path = os.path.join(folder_path, file)
        Backup_File(old_path)
        if os.path.isfile(old_path):
            
            filename, extension = os.path.splitext(file)

            if filename in file_count:
                file_count[filename] = file_count[filename] + 1
            else:
                file_count[filename] = 1

            if file_count[filename] > 1:

                number = file_count[filename] - 1
                new_name = filename + "_" + str(number) + extension
                new_path = os.path.join(folder_path, new_name)

                while os.path.exists(new_path):
                    number = number + 1
                    new_name = filename + "_" + str(number) + extension
                    new_path = os.path.join(folder_path, new_name)

                os.rename(old_path, new_path)
                print(f"rename from {file} to {new_name}")
                print(file, "renamed to", new_name)


