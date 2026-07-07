import json
import os

FILE = "file_data.json" 

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)

def add_history(action, filename):
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    data.append({
        "action": action,
        "file": filename
    })

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def show_history():
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    if not data:
        print("\nNo History Found.")
        return

    print("\n========== FILE HISTORY ==========")
    for i, item in enumerate(data, start=1):
        print("--------------------------------")
        print("Record :", i)
        print("Action :", item["action"])
        print("File   :", item["file"])
    print("--------------------------------")