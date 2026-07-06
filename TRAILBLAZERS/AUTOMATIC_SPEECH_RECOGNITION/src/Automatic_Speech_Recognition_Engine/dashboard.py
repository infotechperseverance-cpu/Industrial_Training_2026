"""
=========================================
Dashboard Module
Purpose:
Provide a centralized interface to monitor
and manage the Smart Voice Assistant.
=========================================
"""

import json
import socket
from datetime import datetime

from speech_recognition_module import check_microphone


# ---------------- Dashboard Heading ----------------
def dashboard_heading():

    print("\n" + "=" * 75)
    print("              SMART VOICE ASSISTANT DASHBOARD")
    print("=" * 75)


# ---------------- Load JSON File ----------------
def load_json(file_name):

    try:

        with open(file_name, "r") as file:

            return json.load(file)

    except Exception:

        return []


# ---------------- Current User ----------------
def show_current_user():

    users = load_json("users.json")

    current_user = "Unknown"

    for user in users:

        if user.get("status") == "Logged In":

            current_user = user.get("username")

            break

    print("\nCurrent User Information")
    print("-" * 75)
    print(f"Username : {current_user}")
    print(f"Date     : {datetime.now().strftime('%d-%m-%Y')}")
    print(f"Time     : {datetime.now().strftime('%I:%M:%S %p')}")


# ---------------- Command History ----------------
def get_command_history():

    return load_json("history.json")


# ---------------- Last Executed Command ----------------
def show_last_command():

    history = get_command_history()

    print("\nLast Executed Command")
    print("-" * 75)

    if len(history) == 0:

        print("No command executed yet.")

        return

    last = history[-1]

    print(f"Command : {last['Command Name']}")
    print(f"Date    : {last['Date']}")
    print(f"Time    : {last['Time']}")
    print(f"Status  : {last['Status']}")


# ---------------- Total Commands ----------------
def show_total_commands():

    history = get_command_history()

    print("\nTotal Executed Commands")
    print("-" * 75)

    print(len(history))


# ---------------- Command Execution History ----------------
def show_command_history():

    history = get_command_history()

    print("\nCommand Execution History")
    print("-" * 75)

    if len(history) == 0:

        print("No command history available.")

        return

    for index, command in enumerate(history, start=1):

        print(
            f"{index}. "
            f"{command['Command Name']} | "
            f"{command['Date']} | "
            f"{command['Time']} | "
            f"{command['Status']}"
        )

# ---------------- Scheduled Commands ----------------
def show_scheduled_commands():

    commands = load_json("scheduled_commands.json")

    print("\nScheduled Commands")
    print("-" * 75)

    if len(commands) == 0:

        print("No scheduled commands available.")

        return

    for command in commands:

        print(
            f"ID : {command['id']} | "
            f"Command : {command['command']} | "
            f"Time : {command['time']} | "
            f"Status : {command['status']}"
        )


# ---------------- Internet Status ----------------
def internet_status():

    try:

        socket.create_connection(("8.8.8.8", 53), timeout=3)

        return "Connected"

    except Exception:

        return "Disconnected"


# ---------------- Microphone Status ----------------
def microphone_status():

    if check_microphone():

        return "Connected"

    return "Disconnected"


# ---------------- System Status ----------------
def show_system_status():

    print("\nSystem Status")
    print("-" * 75)

    print(f"Microphone : {microphone_status()}")

    print(f"Internet   : {internet_status()}")


# ---------------- Notifications ----------------
def show_notifications():
    history = get_command_history()
    print("\nNotifications")
    print("-" * 75)

    if len(history) == 0:
        print("No notifications available.")
        return

    last = history[-1]

    if last["Status"].lower() == "success":
        print(f"✓ SUCCESS : {last['Command Name']} executed successfully.")
    else:
        print(f"✗ FAILED  : {last['Command Name']} execution failed.")


# ---------------- Refresh Dashboard ----------------
def refresh_dashboard():
    print("\nRefreshing dashboard...\n")
    show_dashboard()

# ---------------- Display Dashboard ----------------
def show_dashboard():

    dashboard_heading()

    show_current_user()

    show_last_command()

    show_total_commands()

    show_command_history()

    show_scheduled_commands()

    show_system_status()

    show_notifications()

    print("\n" + "=" * 75)
    print("Dashboard Updated Successfully")
    print("=" * 75)
