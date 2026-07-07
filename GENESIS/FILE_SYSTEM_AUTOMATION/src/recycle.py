import os
import json
import shutil

main_dir = "File_Manager"

RECYCLE_FOLDER = os.path.join(main_dir, "Recycle_Bin")
os.makedirs(RECYCLE_FOLDER, exist_ok=True)

recycle_bin_json = os.path.join(main_dir, "recycle_bin.json")


if not os.path.exists(recycle_bin_json):
    with open(recycle_bin_json, "w") as f:
        json.dump({"recycle_bin": []}, f, indent=4)


def load_recycle_bin():
    with open(recycle_bin_json, "r") as file:
        return json.load(file)


def save_recycle_bin(data):
    with open(recycle_bin_json, "w") as file:
        json.dump(data, file, indent=4)

def movetobin(file_path, filename):

    destination = os.path.join(
        RECYCLE_FOLDER,
        filename
    )
    print("Inside movetobin")

    shutil.move(file_path, destination)

    data = load_recycle_bin()

    data["recycle_bin"].append({

        "filename": filename,
        "original_path": file_path

    })

    save_recycle_bin(data)
    print("File moved to Recycle Bin.")

def restore_file(filename):
    from Classify_file import load_data, save_data
    
    data = load_recycle_bin()
    for item in data["recycle_bin"]:

        if item["filename"] == filename:
           
            source = os.path.join(RECYCLE_FOLDER, filename)
            print("Source:", source)
            print("Source exists:", os.path.exists(source))
            destination = item["original_path"]

            if not os.path.exists(source):
                print("File not found in Recycle Bin.")
                return

            # Create the destination folder if it doesn't exist
            os.makedirs(os.path.dirname(destination), exist_ok=True)

            try:
                shutil.move(source, destination)
                active_data = load_data()
                print(type(active_data))
                print(active_data)

                active_data = load_data()

                active_data = load_data()

                active_data.append({
                "filename": filename,
                "category": os.path.relpath(os.path.dirname(destination), main_dir),
                "password": None
                })

                save_data(active_data)
                data["recycle_bin"].remove(item)
                save_recycle_bin(data)

                print("File restored successfully.")
            except Exception as e:
                print("Error restoring file:", e)

            return

    print("File not found in Recycle Bin.")

def show_recycle_bin():
    data = load_recycle_bin()
    if not data["recycle_bin"]:

        print("\nRecycle Bin is Empty.")

        return

    print("\n========== RECYCLE BIN ==========")

    for i, item in enumerate(data["recycle_bin"], start=1):

        print("--------------------------------")
        print("File :", item["filename"])
        print("Path :", item["original_path"])

 