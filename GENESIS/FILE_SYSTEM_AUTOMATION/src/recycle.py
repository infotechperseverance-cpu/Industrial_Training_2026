import os
import json
import shutil

main_dir = "File_Manager"

RECYCLE_FOLDER = os.path.join(main_dir, "Recycle_Bin")
os.makedirs(RECYCLE_FOLDER, exist_ok=True)

FILE = os.path.join(main_dir, "recycle_bin.json")

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump({"recycle_bin": []}, f, indent=4)

def load_data():
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def movetobin(file_path, filename):

    destination = os.path.join(
        RECYCLE_FOLDER,
        filename
    )
    print("Inside movetobin")

    shutil.move(file_path, destination)

    data = load_data()

    data["recycle_bin"].append({

        "filename": filename,
        "original_path": file_path

    })

    save_data(data)

    print("File moved to Recycle Bin.")

def restore_file(filename):

    data = load_data()

    for item in data["recycle_bin"]:

        if item["filename"] == filename:

            source = os.path.join(
                RECYCLE_FOLDER,
                filename
            )

            shutil.move(
                source,
                item["original_path"]
            )

            data["recycle_bin"].remove(item)

            save_data(data)

            print("File restored successfully.")

            return

    print("File not found.")

def show_recycle_bin():
    data = load_data()
    if not data["recycle_bin"]:

        print("\nRecycle Bin is Empty.")

        return

    print("\n========== RECYCLE BIN ==========")

    for i, item in enumerate(data["recycle_bin"], start=1):

        print("--------------------------------")
        print("File :", item["filename"])
        print("Path :", item["original_path"])

 