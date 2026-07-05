import os

def scan_folder(folder_path):
    """
    Scan all files inside the given folder and return a list of file paths.
    """

    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return []

    files = []

    for root, dirs, filenames in os.walk(folder_path):

        for file in filenames:

            full_path = os.path.join(root, file)

            files.append(full_path)

    print(f"Total files found: {len(files)}")

    return files