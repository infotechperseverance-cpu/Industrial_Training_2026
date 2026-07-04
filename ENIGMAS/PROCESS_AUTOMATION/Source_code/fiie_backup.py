import os
import shutil
import pathlib

"""user delete the file then it created backup,like deleting file,
it created directory name as Backupfile like recycledbin
insted of delete file use this function directly, if any missmatch it return false
this function get file add file in backup module, path if not exist """

destination_file = r"D:\Backupfile"
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

        # Create destination path
        destination_path = os.path.join(destination_file, filename)

        # Check duplicate filename
        while os.path.exists(destination_path):
            filename = automatic_name(filename)
            destination_path = os.path.join(destination_file, filename)

        # Move file
        shutil.move(source_file, destination_path)

        print("File moved successfully")
        print("Saved as:", filename)
        print("Location:", destination_path)

        return True

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        return False

    except Exception as e:
        print(e)
        return False

