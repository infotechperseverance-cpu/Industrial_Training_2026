import pathlib

# Detects whether a file with the same name already exists in the target folder.
# Returns True if duplicate exists; otherwise returns False.

# duplication check function
def duplication_files_detection(folder_path, file_path):
    try:

        if folder_path is None or file_path is None:
            print("Folder path and file path are required")
            return False

        folder_path = str(folder_path).strip()
        file_path = str(file_path).strip()

        if folder_path == "" or file_path == "":
            print("Folder path and file path are required")
            return False
       
        folder = pathlib.Path(folder_path)

        # validate folder path
        if not folder.exists():
            print("Wrong path")
            return False

        if not folder.is_dir():
            print("Not a folder")
            return False

        # extract filename from provided file path
        filename = pathlib.Path(file_path).name

        if filename == "":
            print("Invalid file path")
            return False

        # check duplication
        for file in folder.iterdir():

            if not file.is_file():
                continue

            if file.name == filename:
                print(f"{file} is duplicated")
                return True

        print("File is not duplicated")
        return False

    except KeyboardInterrupt:
        print("User keyboard interrupt")
        return False

    except EOFError:
        print("EOF error")
        return False

    except PermissionError:
        print("Permission denied")
        return False

    except OSError:
        print("Operating system error")
        return False

    except Exception:
        print("Something went wrong")
        return False

