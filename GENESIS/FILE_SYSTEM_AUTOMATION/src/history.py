import json
import os

FILE = "file_history.json"

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)

def add_history(action, filename):
    with open(FILE, "r") as f:
        data = json.load(f)

    data.append({
        "action": action,
        "file": filename
    })

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def show_history():

    with open(FILE, "r") as f:
        data = json.load(f)

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