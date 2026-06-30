"""
File Management Automation System
Integrated Academic Project
FR-01 to FR-07
"""

import os
import re
import json
import shutil
import hashlib
import time
from pathlib import Path

WORKSPACE = "FileManagementAutomationSystem"
os.makedirs(WORKSPACE, exist_ok=True)

# =====================
# LOGIN SYSTEM
# =====================

DB_FILE = "password.json"


def hash_value(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    users = {
        "admin": {"password": hash_value("admin@1234"), "role": "Admin"},
        "users": {"password": hash_value("enigmas@123"), "role": "User"}
    }

    with open(DB_FILE, "w", encoding="utf-8") as f:4
    json.dump(users, f, indent=4)

    return users


def login():
    users = load_users_database()

    for _ in range(3):
        u = input("Username: ")
        p = input("Password: ")

        if u in users and users[u]["password"] == hash_value(p):
            print("Login Successful")
            return users[u]["role"]

        print("Invalid Credentials")

    print("Access Denied")
    return None


# =====================
# VALIDATION
# =====================

def validate_filename(filename):
    pattern = r"^[A-Za-z]+(_[A-Za-z]+)*_\d{4}_[vV]\d+(\.[A-Za-z]{2,4})?$"
    return re.fullmatch(pattern, filename)


# =====================
# FILE SYSTEM
# =====================

def create_folder():
    name = input("Enter NEW Folder Name: ").strip()
    path = os.path.join(WORKSPACE, name)

    if os.path.exists(path):
        print("Folder already exists")
    else:
        os.makedirs(path)
        print("Folder created")


def create_file():
    folder = choose_folder()
    if not folder:
        return

    file_name = input("Enter File Name: ")

    if not validate_filename(file_name):
        print("Invalid filename format")
        return

    content = input("Enter File Content: ")

    file_path = os.path.join(folder, file_name)

    with open(file_path, "w") as f:
        f.write(content)

    print("File created")


# =====================
# VIEW
# =====================

def view_workspace():
    for r, d, f in os.walk(WORKSPACE):
        print(r)
        for file in f:
            print("   ", file)


# =====================
# ORGANIZE
# =====================

FILE_TYPES = {
    ".pdf": "Documents/PDF",
    ".docx": "Documents/Word",
    ".jpg": "Pictures",
    ".png": "Pictures",
    ".mp4": "Videos",
    ".py": "Programming/Python"
}


def organize_files(folder):

    if not os.path.exists(folder):
        print("Folder not found")
        return

    for file in os.listdir(folder):
        src = os.path.join(folder, file)

        if not os.path.isfile(src):
            continue

        ext = Path(file).suffix.lower()
        category = FILE_TYPES.get(ext)

        if not category:
            continue

        dest = os.path.join(WORKSPACE, category)
        os.makedirs(dest, exist_ok=True)

        shutil.move(src, os.path.join(dest, file))

    print("Files organized")

    backup_folder(WORKSPACE, os.path.join(WORKSPACE, "AutoBackup"))


# =====================
# SORT
# =====================

def sort_files(folder, choice):

    files = [f for f in os.listdir(folder)
             if os.path.isfile(os.path.join(folder, f))]

    if choice == 1:
        files.sort()
    elif choice == 2:
        files.sort(reverse=True)

    for f in files:
        print(f)


# =====================
# BACKUP
# =====================

def backup_folder(source, backup):

    os.makedirs(backup, exist_ok=True)

    for file in os.listdir(source):
        src = os.path.join(source, file)

        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(backup, file))

    print("Backup completed")


# =====================
# DUPLICATES
# =====================

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def detect_duplicates(folder):

    seen = {}
    duplicates = []

    for r, d, f in os.walk(folder):
        for file in f:
            path = os.path.join(r, file)
            h = file_hash(path)

            if h in seen:
                duplicates.append(path)
            else:
                seen[h] = path

    for d in duplicates:
        print("Duplicate:", d)


# =====================
# RECYCLE BIN
# =====================

RECYCLE_BIN = os.path.join(WORKSPACE, "RecycleBin")
os.makedirs(RECYCLE_BIN, exist_ok=True)


def delete_to_recycle(file_path):

    if not os.path.exists(file_path):
        print("File not found")
        return

    shutil.move(file_path,
                os.path.join(RECYCLE_BIN, os.path.basename(file_path)))

    print("Moved to recycle bin")


def restore_file(name):

    src = os.path.join(RECYCLE_BIN, name)

    if os.path.exists(src):
        shutil.move(src, WORKSPACE)
        print("Restored")
    else:
        print("Not found")


# =====================
# HELPERS
# =====================

def list_folders():
    return [os.path.join(r, d)
            for r, dlist, _ in os.walk(WORKSPACE)
            for d in dlist]


def choose_folder():
    folders = list_folders()

    if not folders:
        print("No folders found")
        return None

    print("\nFolders:")
    for i, f in enumerate(folders, 1):
        print(i, f)

    try:
        return folders[int(input("Select: ")) - 1]
    except:
        print("Invalid")
        return None


# =====================
# DELETE FIX (YOUR REQUEST)
# =====================

def delete_menu():

    folder = choose_folder()
    if not folder:
        return

    files = [f for f in os.listdir(folder)
             if os.path.isfile(os.path.join(folder, f))]

    if not files:
        print("No files in folder")
        return

    print("\nFiles:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    try:
        choice = int(input("Select file number: "))
        file_path = os.path.join(folder, files[choice - 1])
        delete_to_recycle(file_path)
    except:
        print("Invalid selection")


# =====================
# MAIN MENU
# =====================

def main_menu(role):

    while True:

        print("""
========== File Management System ==========

1. Create New Folder
2. Create New File
3. Organize Files
4. Validate File Name
5. Sort Files
6. Backup Files
7. Duplicate File Analysis
8. Delete File
9. Restore Deleted File
10. View Files
11. Exit

============================================
""")
        c = input("Choice: ")

        if c == "1":
            create_folder()

        elif c == "2":
            create_file()

        elif c == "3":
            folder = choose_folder()
            if folder:
                organize_files(folder)

        elif c == "4":
            print("Valid" if validate_filename(input("File: ")) else "Invalid")

        elif c == "5":
            folder = choose_folder()
            if folder:
                sort_files(folder, int(input("1/2: ")))

        elif c == "6":
            if role == "Admin":
                folder = choose_folder()
                if folder:
                    backup_folder(folder, os.path.join(WORKSPACE, "Backup"))

        elif c == "7":
            folder = choose_folder()
            if folder:
                detect_duplicates(folder)

        elif c == "8":
            if role == "Admin":
                delete_menu()
            else:
                print("Denied")

        elif c == "9":
            if role == "Admin":
                restore_file(input("File name: "))

        elif c == "10":
            view_workspace()

        elif c == "11":
            break


# =====================
# RUN
# =====================

if __name__ == "__main__":
    role = login()
    if role:
        main_menu(role)