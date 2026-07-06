import json
import threading
import time
from datetime import datetime
from speech_recognition_module import listen
from voice_engine import speak
from commandHistory import save_command
from config import SCHEDULE_FILE


# ------------------ FILE ------------------
file_name = SCHEDULE_FILE
my_commands = []

log_file = "system_logs.txt"


def write_log(message):
    try:
        with open(log_file, "a") as file:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{current_time}] {message}\n")
    except Exception as e:
        print(e)


# ------------------ LOAD DATA ------------------
def load_data():
    global my_commands
    try:
        with open(file_name, "r") as f:
            my_commands = json.load(f)
    except Exception as e:
        print(e)
        my_commands = []


# ------------------ SAVE DATA ------------------
def save_data():
    with open(file_name, "w") as f:
        json.dump(my_commands, f, indent=4)

# ------------------ DATE VALIDATION ------------------
def validate_time(user_time):
    try:
        dt = datetime.strptime(user_time, "%Y-%m-%d %H:%M")
        if dt < datetime.now():
            return None
        return dt
    except:
        return None


# ------------------ ADD COMMAND ------------------
def add_command():
    print("\nChoose Input Method")
    print("1. Voice")
    print("2. Text")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        cmd = listen()
    elif choice == "2":
        cmd = input("Enter Command: ").strip()
    else:
        print("Invalid choice")
        speak("Invalid choice")
        return

    if cmd is None or cmd.strip() == "":
        print("❌ Invalid command")
        speak("Invalid command")
        return



    time_input = input("Enter date & time (YYYY-MM-DD HH:MM): ").strip()
    valid = validate_time(time_input)

    # Check duplicate command
    for c in my_commands:
        if (c["command"].strip().lower() == cmd.strip().lower() and
                c["time"] == time_input and
                c["status"] == "pending"):
            print("❌ This command is already scheduled for the same time.")
            speak("This command is already scheduled.")
            write_log("Duplicate command scheduling attempted.")
            return


    if valid is None:
        print("❌ Invalid date/time")
        speak("Invalid date time")
        return

    if my_commands:
        cmd_id = max(c["id"] for c in my_commands) + 1
    else:
        cmd_id = 1

    my_commands.append({
        "id": cmd_id,
        "command": cmd,
        "time": time_input,
        "status": "pending"
    })

    save_data()
    print("✅ Command scheduled")
    speak("Command scheduled successfully")
    write_log(f"Command added: {cmd} at {time_input}")



# ------------------ VIEW COMMANDS ------------------
def view_commands():
    if len(my_commands) == 0:
        print("⚠ No scheduled commands")
        speak("No commands found")
        return

    print("\n------ SCHEDULED COMMANDS ------")
    for c in my_commands:
        print(f"ID: {c['id']} | CMD: {c['command']} | TIME: {c['time']} | STATUS: {c['status']}")
    print("--------------------------------\n")


# ------------------ EDIT COMMAND ------------------
def edit_command():
    view_commands()

    try:
        cid = int(input("Enter ID to edit: "))
    except:
        print("❌ Invalid ID")
        return

    for c in my_commands:
        if c["id"] == cid:

            print("\nChoose Input Method")
            print("1. Voice")
            print("2. Text")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                new_cmd = listen()
            elif choice == "2":
                new_cmd = input("Enter New Command: ").strip()
            else:
                print("Invalid choice")
                speak("Invalid choice")
                return

            if new_cmd is None or new_cmd.strip() == "":
                print("Invalid command")
                speak("Invalid command")
                return


            new_time = input("Enter new date & time (YYYY-MM-DD HH:MM): ").strip()
            valid = validate_time(new_time)

            if valid is None:
                print("❌ Invalid time")
                speak("Invalid time")
                return

            c["command"] = new_cmd
            c["time"] = new_time
            c["status"] = "pending"

            save_data()
            print("✅ Updated successfully")
            speak("Command updated")
            write_log(f"Command edited ID {cid}")
            return

    print("❌ ID not found")
    speak("ID not found")


# ------------------ DELETE COMMAND ------------------
def delete_command():
    view_commands()

    try:
        cid = int(input("Enter ID to delete: "))
    except:
        print("❌ Invalid ID")
        return

    for c in my_commands:
        if c["id"] == cid:
            my_commands.remove(c)
            for i in range(len(my_commands)):
                my_commands[i]["id"] = i + 1
            save_data()
            print("✅ Deleted successfully")
            speak("Command deleted")
            write_log(f"Command deleted ID {cid}")
            return

    print("❌ ID not found")
    speak("ID not found")


# ------------------ EXECUTE COMMAND ------------------

def execute_command(cmd):
    try:
        from command_processing import process_command

        print(f"\nExecuting: {cmd}")

        speak(f"Executing {cmd}")

        process_command(cmd)

        save_command(cmd, "Success")

        write_log(f"Executed command: {cmd}")

        return True

    except Exception as e:
        print(e)

        speak("Command execution failed")

        save_command(cmd, "Failed")

        write_log(f"Failed command: {cmd}")

        return False


# ------------------ AUTO EXECUTOR ------------------
def auto_runner():
    # Load saved commands when module starts
    load_data()
    while True:
        now = datetime.now()

        for c in my_commands:
            if c["status"] == "pending":
                cmd_time = datetime.strptime(c["time"], "%Y-%m-%d %H:%M")

                if now >= cmd_time:
                    if execute_command(c["command"]):
                        c["status"] = "done"
                        save_data()

                        speak("Your scheduled command has been executed")

        time.sleep(1)

def start_sound():
    speak("Voice command scheduler activated")


def exit_sound():
    speak("Voice command scheduler exiting")


