import os
from datetime import datetime
from Classify_file import load_data, main_dir




def load_files(sort_by="name_az"):

    records = load_data()

    files = []

    for item in records:

        full_path = os.path.join(
            main_dir,
            item["category"],
            item["filename"]
        )

        if os.path.isfile(full_path):

            files.append({

                "name": item["filename"],
                "category": item["category"],
                "type": os.path.splitext(item["filename"])[1].upper(),
                "size": os.path.getsize(full_path),
                "created": os.path.getctime(full_path),
                "modified": os.path.getmtime(full_path)

            })
        

    # Sorting Options
    if sort_by == "name_az":
        files.sort(key=lambda x: x["name"].lower())

    elif sort_by == "name_za":
        files.sort(key=lambda x: x["name"].lower(), reverse=True)

    elif sort_by == "type":
        files.sort(key=lambda x: x["type"])

    elif sort_by == "size":
        files.sort(key=lambda x: x["size"])

    elif sort_by == "created":
        files.sort(key=lambda x: x["created"])

    elif sort_by == "modified":
        files.sort(key=lambda x: x["modified"])

    elif sort_by == "oldest":
        files.sort(key=lambda x: x["modified"])

    elif sort_by == "newest":
        files.sort(key=lambda x: x["modified"], reverse=True)

    print("\n========== SORTED FILES ==========")

    for f in files:

        print("--------------------------------")
        print("Name      :", f["name"])
        print("Category  :", f["category"])
        print("Type      :", f["type"])
        print("Size      :", f["size"], "Bytes")
        print("Created   :", datetime.fromtimestamp(f["created"]).strftime("%d-%m-%Y %H:%M"))
        print("Modified  :", datetime.fromtimestamp(f["modified"]).strftime("%d-%m-%Y %H:%M"))

        print("--------------------------------")

def sorting_menu():

    while True:

        print("\n========== SORT FILES ==========")
        print("1. Name (A-Z)")
        print("2. Name (Z-A)")
        print("3. File Type")
        print("4. File Size")
        print("5. Newest")
        print("6. Oldest")
        print("7. Exit")

        choice = int(input("Enter Choice: "))

        if choice == 1:
            load_files("name_az")

        elif choice == 2:
            load_files("name_za")

        elif choice == 3:
            load_files("type")

        elif choice == 4:
            load_files("size")

        elif choice == 5:
            load_files("newest")

        elif choice == 6:
            load_files("oldest")

        elif choice == 7:
            break

        else:
            print("Invalid Choice")



