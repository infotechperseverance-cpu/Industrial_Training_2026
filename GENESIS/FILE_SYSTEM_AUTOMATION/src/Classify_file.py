import pwinput
import os
import json
from pathlib import Path
from file_history import add_history


main_dir = "File_Manager"
json_file = os.path.join(main_dir, "file_data.json")

os.makedirs(main_dir, exist_ok=True)

Folders = [
    "Documents/PDF",
    "Documents/Word",
    "Documents/Excel",
    "Documents/PowerPoint",

    "Media/Pictures",
    "Media/Videos",
    "Media/Audio",

    "Programming/C",
    "Programming/C++",
    "Programming/Python",
    "Programming/Java",
    "Programming/HTML",
    "Programming/CSS",
    "Programming/JavaScript",

    "Others"
]

for folder in Folders:
    os.makedirs(os.path.join(main_dir, folder), exist_ok=True)


# ---------------- JSON Functions ----------------


def load_data():


    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            return json.load(file)
    return []


def save_data(data):
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)


# ---------------- File Classification ----------------

def classification_file(filename):

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        return "Documents/PDF"

    elif extension in [".doc", ".docx"]:
        return "Documents/Word"

    elif extension in [".xls", ".xlsx"]:
        return "Documents/Excel"

    elif extension in [".ppt", ".pptx"]:
        return "Documents/PowerPoint"

    elif extension in [".jpg", ".jpeg", ".png", ".gif"]:
        return "Media/Pictures"

    elif extension in [".mp4", ".mkv"]:
        return "Media/Videos"

    elif extension in [".mp3", ".wav"]:
        return "Media/Audio"

    elif extension == ".c":
        return "Programming/C"

    elif extension in [".cpp", ".cc", ".cxx"]:
        return "Programming/C++"

    elif extension == ".py":
        return "Programming/Python"

    elif extension == ".java":
        return "Programming/Java"

    elif extension == ".html":
        return "Programming/HTML"

    elif extension == ".css":
        return "Programming/CSS"

    elif extension == ".js":
        return "Programming/JavaScript"

    else:
        return "Others"


# ---------------- Create File ----------------

def create_file(filename,password):

    category = classification_file(filename)

    folder_path = os.path.join(main_dir, category)

    path = os.path.join(folder_path, filename)

    if os.path.exists(path):
        print("File already exists.")
        return

    with open(path, "w") as file:
        file.write("hello, file is created")

    data = load_data()
    
    
    data.append({
        "filename": filename,
        "category": category,
        "password": password
    })

    save_data(data)
    add_history("Create", filename)

    print(f"The '{filename}' is created successfully.")

# ---------------- Rename File ----------------

def rename_file(old_name, new_name):

    data = load_data()
    
    for item in data:

        if item["filename"] == old_name:

            # Check extension
            old_ext = os.path.splitext(old_name)[1].lower()
            new_ext = os.path.splitext(new_name)[1].lower()
           
            if old_ext != new_ext:
                print("Extension cannot be changed while renaming.")
                return

            old_category = item["category"]
            old_path = os.path.join(main_dir, old_category, old_name)

            new_category = classification_file(new_name)
            new_folder = os.path.join(main_dir, new_category)
            new_path = os.path.join(new_folder, new_name)
            

            if not os.path.exists(old_path):
                print("File not found.")
                return

            if os.path.exists(new_path):
                print("A file with the new name already exists.")
                return

            os.rename(old_path, new_path)

            item["filename"] = new_name
            item["category"] = new_category

            save_data(data)
            add_history("Rename", f"{old_name} -> {new_name}")

            print("File renamed successfully.")
            return

    print("File not found.")

# ---------------- Delete File ----------------

def delete_file(filename):

    data = load_data()

    for item in data:
        if item["filename"] == filename:

            # If the file is password protected
            if item.get("password"):
                entered_password = pwinput.pwinput("Enter Password: ")

                if entered_password != item["password"]:
                    print("Incorrect password. File cannot be deleted.")
                    return

            # Delete the physical file
            
            category = item["category"]
            folder_path = os.path.join(main_dir, category)
            file_path = os.path.join(folder_path, filename)
            
            print("File path:", file_path)
            print("Exists:", os.path.exists(file_path))

            if os.path.exists(file_path):
               from recycle import movetobin
               movetobin(file_path,filename)
               print("Moved to Recycle Bin")
            else:
               print("Physical file not found.")
            # Remove record from JSON
            data.remove(item)
            save_data(data)

            print("File deleted successfully.")
            return

    print("File not found.")


# ---------------- Display Records ----------------

def display_records():

    data = load_data()

    if not data:
        print("\nNo records found.")
        return

    print("\n========== STORED FILE RECORDS ==========")

    count = 1

    for item in data:

        print("--------------------------------------")
        print("Record   :", count)
        print("Filename :", item["filename"])
        print("Category :", item["category"])
        password = item.get("password", "")

        if password:
         print("Password : Protected")
        else:
         print("Password : Not Protected")
    
        count += 1

    print("--------------------------------------")