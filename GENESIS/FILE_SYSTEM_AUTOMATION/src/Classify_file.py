import os
import json
import shutil
from pathlib import Path
import re

main_dir= "File_Manager"
json_file=os.path.join(main_dir,"file_data.json")

os.makedirs(main_dir,exist_ok=True)
Folders= [
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
    os.makedirs(os.path.join(main_dir,folder), exist_ok=True)

def load_data():
    if os.path.exists(json_file):
        with open(json_file,"r")as file:
            return json.load(file)
    return[]
def save_data(data):
    with open(json_file,"w")as file:
        json.dump(data,file,indent=4)


def create_file(filename):
    
    path=os.path.join(main_dir,filename)
    with open(path,"w")as file:
        file.write("hello,file is created")
    print(f"The'{filename}'is created succesfully.")

def classification_file (filename):
   extension=Path(filename).suffix.lower()
    
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


# file rename function        


def rename_file(old_name, new_name):

    data = load_data()

    # Search for the file in JSON records
    for item in data:
        if item["filename"] == old_name:

            category = item["category"]

            old_path = os.path.join(main_dir, category, old_name)
            new_path = os.path.join(main_dir, category, new_name)

            if os.path.exists(old_path):
                os.rename(old_path, new_path)

                # Update JSON
                item["filename"] = new_name
                save_data(data)

                print("File renamed successfully.")
                return True

            else:
                print("File not found.")
                return False

    print("File not found.")
    return False

def delete_file(filename):
    
    category = classification_file(filename)
    path = os.path.join(main_dir, category, filename)

    if os.path.exists(path):
        os.remove(path)

        data = load_data()
        data = [item for item in data if item["filename"] != filename]
        save_data(data)

        print("File deleted successfully.")
    else:
        print("File not found.")

# ---------------- Display JSON Records ----------------
def display_records():

    data = load_data()

    if not data:
        print("\nNo records found.")
        return

    print("\nStored File Records")

    for item in data:
        print("----------------------------")
        print("Filename :", item["filename"])
        print("Category :", item["category"])
