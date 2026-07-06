"""
=========================================
Command History Module
Purpose:
Stores and displays executed command history.
=========================================
"""

import json
import os
from datetime import datetime
from config import HISTORY_FILE


# Create history.json file if it does not exist
def create_history_file():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as file:
            json.dump([], file, indent=4)


# Save executed command details in history.json
def save_command(command_name, status):

    create_history_file()

    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

    except json.JSONDecodeError:
        history = []

    now = datetime.now()

    command = {
        "Command Name": command_name,
        "Date": now.strftime("%d-%m-%Y"),
        "Time": now.strftime("%H:%M:%S"),
        "Status": status
    }

    history.append(command)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


# Display all saved command history
def view_history():

    create_history_file()

    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

    except json.JSONDecodeError:
        history = []

    if len(history) == 0:
        print("\nNo Command History Found.\n")
        return

    print("\n========== COMMAND HISTORY ==========\n")

    for i, item in enumerate(history, start=1):

        print(f"{i}. Command Name : {item['Command Name']}")
        print(f"   Date         : {item['Date']}")
        print(f"   Time         : {item['Time']}")
        print(f"   Status       : {item['Status']}")
        print()