import os
import shutil
import pathlib
from filehandling import read_json, update_json

destination_file = os.path.join(os.getcwd(), "Backupfile")
metadata_file = os.path.join(destination_file, "backup_metadata.json")
"""
BACKUP MODULE
Backs up a file by copying it (original stays untouched).
- Same file backed up again -> skips, tells you it's already backed up.
- Different file, same name -> saved as name(1), name(2), etc.
- Restore_File() puts a backed up file back to where it came from.
"""

def automatic_name(filename):
    print("Automatic rename file name with sequence")

    try:
        # File with extension
        if "." in filename:
            index = filename.rfind(".")

            text1 = filename[:index]
            text2 = filename[index:]

            # Check if already ends with "(number)"
            if text1.endswith(")"):
                start = text1.rfind("(")

                if start != -1:
                    number = text1[start + 1:-1]

                    if number.isdigit():
                        filename = (
                            text1[:start]
                            + f"({int(number) + 1})"
                            + text2
                        )
                        print("Automatic rename file name as", filename)
                        return filename

            filename = text1 + "(1)" + text2
            print("Automatic rename file name as", filename)
            return filename

        # File without extension
        else:
            if filename.endswith(")"):
                start = filename.rfind("(")

                if start != -1:
                    number = filename[start + 1:-1]

                    if number.isdigit():
                        filename = (
                            filename[:start]
                            + f"({int(number) + 1})"
                        )
                        print("Automatic rename file name as", filename)
                        return filename

            filename = filename + "(1)"
            print("Automatic rename file name as", filename)
            return filename

    except Exception:
        print("Something went wrong")
        return filename


def Backup_File(source_file):
    try:
        # Create backup folder if not exists
        if os.path.isdir(destination_file):
            pass
        else:
            os.mkdir(destination_file)

        # Validate source file
        if not os.path.exists(source_file):
            print(f"{source_file} is invalid")
            return False

        # Get original filename
        filename = os.path.basename(source_file)

        source_path_full = os.path.abspath(source_file)

        # Check if this exact file is already backed up (by original path,
        # not just by name) - if so, dont create another copy
        metadata = read_json(metadata_file)

        for backup_name, original_path in metadata.items():
            if original_path == source_path_full:
                existing_path = os.path.join(destination_file, backup_name)
                if os.path.exists(existing_path):
                    print("File is already backed up")
                    print("Saved as:", backup_name)
                    print("Location:", existing_path)
                    return True

         
        destination_path = os.path.join(destination_file, filename)

        
        while os.path.exists(destination_path):
            filename = automatic_name(filename)
            destination_path = os.path.join(destination_file, filename)

        # Copy file
        shutil.copy2(source_file, destination_path)

        # Remember where this file originally came from, for restoring later
        update_json(metadata_file, filename, os.path.abspath(source_file))

        print("File backed up successfully")
        print("Saved as:", filename)
        print("Location:", destination_path)

        return True

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        return False

    except Exception as e:
        print(e)
        return False


def Restore_File(backup_filename):
    try:
        # Validate the backed up file exists
        backup_path = os.path.join(destination_file, backup_filename)

        if not os.path.exists(backup_path):
            print(f"{backup_filename} is invalid")
            return False

        # Look up where it originally came from
        metadata = read_json(metadata_file)

        if backup_filename not in metadata:
            print("Original location for this file is unknown")
            return False

        original_path = metadata[backup_filename]
        original_folder = os.path.dirname(original_path)

        # Validate original folder still exists
        if not os.path.exists(original_folder):
            print(f"{original_folder} is invalid")
            return False

        filename = os.path.basename(original_path)
        restore_path = os.path.join(original_folder, filename)

        # Check duplicate filename - rename in sequence, never replace
        while os.path.exists(restore_path):
            filename = automatic_name(filename)
            restore_path = os.path.join(original_folder, filename)

        # Copy file back (paste) instead of move
        shutil.copy2(backup_path, restore_path)

        print("File restored successfully")
        print("Saved as:", filename)
        print("Location:", restore_path)

        return True

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        return False

    except Exception as e:
        print(e)
        return False
