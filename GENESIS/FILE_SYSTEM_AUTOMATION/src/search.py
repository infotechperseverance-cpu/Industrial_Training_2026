import os
import json
import difflib
from datetime import datetime

# ---------------- File Paths ----------------

main = "File_Manager"

FILE_DATA = os.path.join(main, "file_data.json")

BACKUP_LOG = "backup_log.json"

SEARCH_HISTORY = "search_history.json"

# ---------------- Load File Records ----------------

def load_file():

    if os.path.exists(FILE_DATA):

        with open(FILE_DATA, "r") as file:

            return json.load(file)

    return []

# ---------------- Load Backup Records ----------------

def load_backup():

    if os.path.exists(BACKUP_LOG):

        with open(BACKUP_LOG, "r") as file:

            return json.load(file)

    return {"backups": []}

# ---------------- Load Search History ----------------

def load_search_history():

    if os.path.exists(SEARCH_HISTORY):

        with open(SEARCH_HISTORY, "r") as file:

            return json.load(file)

    return []

# ---------------- Save Search History ----------------

def save_search_history(data):

    with open(SEARCH_HISTORY, "w") as file:

        json.dump(data, file, indent=4)

# ---------------- Add Search History ----------------

def add_history(keyword, result):

    history = load_search_history()

    history.append({

        "keyword": keyword,

        "result": result,

        "date": datetime.now().strftime("%d-%m-%Y"),

        "time": datetime.now().strftime("%H:%M:%S")

    })

    save_search_history(history)

# ---------------- Display Search History ----------------

def display_history():

    history = load_search_history()

    if not history:

        print("\nNo Search History Found.")

        return

    print("\n========== SEARCH HISTORY ==========\n")

    for item in history:

        print("Keyword :", item["keyword"])

        print("Result  :", item["result"])

        print("Date    :", item["date"])

        print("Time    :", item["time"])

        print("-------------------------------------")

# ---------------- Clear Search History ----------------

def clear_history():

    save_search_history([])

    print("\nSearch History Cleared Successfully.")

# ---------------- Display File Information ----------------

def display_file(item):

    filename = item["filename"]

    category = item["category"]

    path = os.path.join(main, category, filename)

    print("\n------------------------------------")

    print("Filename :", filename)

    print("Category :", category)

    print("Location :", path)

    if os.path.exists(path):

        print("Size     :", os.path.getsize(path), "Bytes")

    else:

        print("Size     : File Not Found")

    print("------------------------------------")

# ---------------- Search by Exact File Name ----------------

def search_by_filename():

    filename = input("\nEnter File Name : ").strip()

    data = load_file()

    found = False

    for item in data:

        if item["filename"].lower() == filename.lower():

            display_file(item)

            add_history(filename, "Found")

            found = True

            break

    if not found:

        print("\nFile Not Found.")

        suggestion(filename)

        add_history(filename, "Not Found")

# ---------------- Search by Partial Name ----------------

def search_by_partial_name():

    keyword = input("\nEnter Keyword : ").strip().lower()

    data = load_file()

    found = False

    print("\nMatching Files\n")

    for item in data:

        if keyword in item["filename"].lower():

            display_file(item)

            found = True

    if found:

        add_history(keyword, "Found")

    else:

        print("No Matching Files Found.")

        add_history(keyword, "Not Found")

# ---------------- Search by Extension ----------------

def search_by_extension():

    extension = input("\nEnter Extension (pdf,py,jpg...) : ")

    extension = "." + extension.lower().replace(".", "")

    data = load_file()

    found = False

    print("\nMatching Files\n")

    for item in data:

        if item["filename"].lower().endswith(extension):

            display_file(item)

            found = True

    if found:

        add_history(extension, "Found")

    else:

        print("No Files Found.")

        add_history(extension, "Not Found")

# ---------------- Search by Category ----------------

def search_by_category():

    category = input("\nEnter Category : ").strip().lower()

    data = load_file()

    found = False

    print("\nMatching Files\n")

    for item in data:

        if category in item["category"].lower():

            display_file(item)

            found = True

    if found:

        add_history(category, "Found")

    else:

        print("Category Not Found.")

        add_history(category, "Not Found")

# ---------------- Search by File Size ----------------

def search_by_size():

    try:

        size = int(input("\nEnter Minimum File Size (Bytes): "))

    except:

        print("Invalid Size.")

        return

    data = load_file()

    found = False

    print("\nMatching Files\n")

    for item in data:

        filename = item["filename"]

        category = item["category"]

        path = os.path.join(main, category, filename)

        if os.path.exists(path):

            if os.path.getsize(path) >= size:

                display_file(item)

                found = True

    if found:

        add_history(str(size), "Found")

    else:

        print("No Files Found.")

        add_history(str(size), "Not Found")

# ---------------- Smart Suggestions ----------------

def suggestion(filename):

    data = load_file()

    file_list = []

    for item in data:

        file_list.append(item["filename"])

    result = difflib.get_close_matches(filename, file_list, n=5, cutoff=0.4)

    if result:

        print("\nDid You Mean?")

        for name in result:

            print("->", name)

# ---------------- Recent Files ----------------

def recent_files():

    data = load_file()

    files = []

    for item in data:

        filename = item["filename"]

        category = item["category"]

        path = os.path.join(main, category, filename)

        if os.path.exists(path):

            files.append((os.path.getctime(path), item))

    files.sort(reverse=True)

    print("\n========== RECENT FILES ==========\n")

    for created, item in files[:5]:

        display_file(item)

# ---------------- Recent Backups ----------------

def recent_backups():

    backups = load_backup()

    records = backups.get("backups", [])

    if not records:

        print("\nNo Backup Records Found.")

        return

    print("\n========== RECENT BACKUPS ==========\n")

    count = 0

    for item in reversed(records):

        print("File Name :", item["file_name"])

        print("Date      :", item["date"])

        print("Time      :", item["time"])

        print("Status    :", item["status"])

        print("-------------------------------------")

        count += 1

        if count == 5:

            break

# ---------------- Smart Search Menu ----------------

def search_menu():

    while True:

        print("\n========================================")
        print("          SMART SEARCH SYSTEM")
        print("========================================")
        print("1. Search by Exact File Name")
        print("2. Search by Partial File Name")
        print("3. Search by Extension")
        print("4. Search by Category")
        print("5. Search by File Size")
        print("6. Recent Files")
        print("7. Recent Backups")
        print("8. Display Search History")
        print("9. Clear Search History")
        print("10. Exit")
        print("========================================")

        try:

            choice = int(input("Enter Your Choice : "))

        except:

            print("Invalid Choice.")
            continue

        match choice:

            case 1:
                search_by_filename()

            case 2:
                search_by_partial_name()

            case 3:
                search_by_extension()

            case 4:
                search_by_category()

            case 5:
                search_by_size()

            case 6:
                recent_files()

            case 7:
                recent_backups()

            case 8:
                display_history()

            case 9:
                clear_history()

            case 10:

                print("\nReturning To Main Menu...")
                break

            case _:

                print("Invalid Choice.")