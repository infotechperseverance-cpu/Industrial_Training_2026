import json
import threading
import time
from datetime import datetime
import speech_recognition as sr
import pyttsx3


# ------------------ FILE ------------------
file_name = "scheduled_commands.json"
my_commands = []

# ------------------ SPEECH ENGINE ------------------
engine = pyttsx3.init()
engine.setProperty('rate', 160)

log_file = "system_logs.txt"


def write_log(message):
    try:
        with open(log_file, "a") as f:
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{time_now}] {message}\n")
    except:
        print("❌ Logging failed")


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    # ----------------- SET FEMALE VOICE FIRST ------------------
    voices = engine.getProperty('voices')

    female_found = False

    for v in voices:
        if "zira" in v.name.lower() or "hazel" in v.name.lower() or "female" in v.name.lower():
            engine.setProperty('voice', v.id)
            female_found = True
            break

    # fallback if female voice not found
    if not female_found and len(voices) > 0:
        engine.setProperty('voice', voices[0].id)

    # ----------------- NOW SPEAK ------------------
    engine.say(text)
    engine.runAndWait()

# ------------------ LOAD DATA ------------------
def load_data():
    global my_commands
    try:
        with open(file_name, "r") as f:
            my_commands = json.load(f)
    except:
        my_commands = []


# ------------------ SAVE DATA ------------------
def save_data():
    with open(file_name, "w") as f:
        json.dump(my_commands, f, indent=4)


# ------------------ VOICE INPUT ------------------
def voice_input():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Speak command...")
            speak("Speak your command")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5)

        text = r.recognize_google(audio)
        print("📝 You said:", text)
        return text

    except:
        print("❌ Voice error")
        speak("Sorry, I could not understand")
        return None


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
    cmd = voice_input()

    if cmd is None or cmd.strip() == "":
        print("❌ Invalid command")
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

    cmd_id = len(my_commands) + 1

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

            new_cmd = voice_input()
            if new_cmd is None:
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
    print(f"\n🚀 Executing: {cmd}")
    speak(f"Executing your command {cmd}")
    write_log(f"Executed command: {cmd}")


# ------------------ AUTO EXECUTOR ------------------
def auto_runner():
    while True:
        now = datetime.now()

        for c in my_commands:
            if c["status"] == "pending":
                cmd_time = datetime.strptime(c["time"], "%Y-%m-%d %H:%M")

                if now >= cmd_time:
                    execute_command(c["command"])
                    c["status"] = "done"
                    save_data()

                    speak("Your scheduled command has been executed")

        time.sleep(10)

def start_sound():
    speak("Voice command scheduler activated")


def exit_sound():
    speak("Voice command scheduler exiting")

1
def main_menu():
    load_data()

    t = threading.Thread(target=auto_runner, daemon=True)
    t.start()

    # 🔊 START SOUND
    start_sound()

    while True:
        print("\n====== VOICE COMMAND SCHEDULER ======")
        print("1. Add Command (Voice)")
        print("2. View Commands")
        print("3. Edit Command (Voice)")
        print("4. Delete Command")
        print("5. Exit")
        print("=====================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_command()
        elif choice == "2":
            view_commands()
        elif choice == "3":
            edit_command()
        elif choice == "4":
            delete_command()
        elif choice == "5":
            exit_sound()
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice")
            speak("Invalid choice")


if __name__ == "__main__":
    main_menu()