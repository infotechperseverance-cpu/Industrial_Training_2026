import os

def scan_folder(folder_path):
    """
    Scan all files inside the given folder and return a list of file paths.
    """

    # Check for empty input
    if not folder_path or folder_path.strip() == "":
        print("Folder Name Cannot be Empty")
        return []

    # Check if path exists
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return []

    # Check if path is a directory
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Input must be a folder.")
        return []

    files = []

    for root, dirs, filenames in os.walk(folder_path):
        for file in filenames:
            full_path = os.path.join(root, file)
            files.append(full_path)

    print(f"Total files found: {len(files)}")
    return files
