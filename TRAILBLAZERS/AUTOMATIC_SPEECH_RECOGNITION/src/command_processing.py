"""
=========================================
Command Processing Module
Purpose:
Compare voice commands with predefined
commands and execute the required module.
=========================================
"""
from voice_calculator import  is_math_command
import json
import importlib
from voice_calculator import process_calculation
from speech_recognition_module import listen
from voice_engine import speak
from commandHistory import save_command


# ---------------- COMMAND FILE ----------------
COMMAND_FILE = "commands.json"


# ---------------- LOAD COMMANDS ----------------
def load_commands():

    try:

        with open(COMMAND_FILE, "r") as file:

            return json.load(file)

    except Exception as e:

        print("Error loading commands:", e)

        return []


# ---------------- SHOW HELP ----------------
def show_help():

    commands = load_commands()

    print("\n========== AVAILABLE COMMANDS ==========\n")

    for cmd in commands:

        if cmd["type"] in ["exact", "dynamic"]:

            print("-", cmd["command"])

    print("\n========================================")

    speak("These are the available commands.")


# ---------------- FIND COMMAND ----------------
def find_command(user_command):

    commands = load_commands()

    user_command = user_command.strip().lower()

    for command in commands:

        if command["type"] == "exact":

            if command["command"] == user_command:

                return command

        elif command["type"] == "dynamic":

            if user_command.startswith(command["command"]):

                return command


        elif command["type"] == "confirmation_required":

            if command["command"] == user_command:
                return command

    return None


# ---------------- GET RESPONSE ----------------
def get_response(command):
    return command.get("response", "")

# ---------------- EXECUTE ACTION ----------------
def execute_action(command_data):

    try:

        module_name = command_data["module"]

        action_name = command_data["action"]

        response = command_data["response"]

        module = importlib.import_module(module_name)

        action = getattr(module, action_name)

        # -------- Dynamic Commands --------
        if command_data["type"] == "dynamic":

            return action

        # -------- Confirmation Commands --------
        if command_data["type"] == "confirmation_required":
            return action

        # -------- Exact Commands --------
        result = action()

        if result:
            save_command(command_data["command"], "Success")

            return True

        save_command(command_data["command"], "Failed")

        return False

    except AttributeError:

        print("Function not found.")

        speak("Function not found.")

        save_command(command_data["command"], "Failed")

        return False

    except ModuleNotFoundError:

        print("Module not found.")

        speak("Module not found.")

        save_command(command_data["command"], "Failed")

        return False

    except Exception as e:

        print(e)

        speak("Sorry, I couldn't complete your request.")

        save_command(command_data["command"], "Failed")

        return False


# ---------------- UNKNOWN COMMAND ----------------
def unknown_command(show_prompt=True):

    speak("Sorry, I didn't understand that command.")

    print("\nUnknown Command.")

    if not show_prompt:
        return False

    choice = input("Show available commands? (yes/no): ").strip().lower()

    if choice == "yes":
        show_help()

    return False

# ---------------- DYNAMIC COMMANDS ----------------

def execute_dynamic(command_data, user_command):

    action = command_data["action"]

    module = importlib.import_module(command_data["module"])


    # -------- Google Search --------
    if action == "google_search":

        query = user_command.replace("search", "", 1).strip()

        if query == "":

            speak("Please tell me what you want to search.")

            return False

        return module.google_search(query)


    # -------- Play Music --------
    elif action == "play_song":

        song = user_command.replace("play music", "", 1).strip()

        if song == "":
            speak("Please tell me which song to play.")
            return False

        return module.play_song(song)



    # -------- Voice Calculator --------
    elif action == "start_voice_calculator":

        expression = user_command.replace("voice calculator", "", 1).strip()

        # If user only said "voice calculator"
        # start calculator mode
        if expression == "":
            return module.start_voice_calculator()

        # If user said "voice calculator five plus six"
        return module.process_calculation(expression)

    else:

        speak("Dynamic command is not supported.")

        return False


# ---------------- CONFIRMATION ----------------

def get_confirmation():
    import assistant_state


    speak("Please say Yes or No.")
    assistant_state.assistant_busy = True
    confirmation = listen()
    assistant_state.assistant_busy = False

    if confirmation is None:

        return None

    confirmation = confirmation.lower()

    if confirmation == "yes":

        return True

    if confirmation == "no":

        return False

    speak("Invalid confirmation.")

    return None


# ---------------- SHUTDOWN ----------------

def handle_shutdown(module):

    result = get_confirmation()

    if result is True:

        return module.shutdown_computer()

    elif result is False:

        speak("Shutdown cancelled.")

        return False

    return False


# ---------------- RESTART ----------------

def handle_restart(module):

    result = get_confirmation()

    if result is True:

        return module.restart_computer()

    elif result is False:

        speak("Restart cancelled.")

        return False

    return False

# ---------------- MAIN PROCESS COMMAND ----------------

def process_command(user_command,interactive=True):

    if user_command is None:

        return False

    user_command = user_command.strip().lower()

    command_data = find_command(user_command)

    if command_data is None:

        if is_math_command(user_command):

            result = process_calculation(user_command)

            if result is not None:
                return True

        return unknown_command(interactive)

    try:

        # -------- Dynamic Commands --------
        if command_data["type"] == "dynamic":

            result = execute_dynamic(command_data, user_command)

        # -------- Shutdown --------
        elif command_data["action"] == "shutdown_computer":

            module = importlib.import_module(command_data["module"])

            result = handle_shutdown(module)

        # -------- Restart --------
        elif command_data["action"] == "restart_computer":

            module = importlib.import_module(command_data["module"])

            result = handle_restart(module)



        # -------- Exact Commands --------
        else:

            result = execute_action(command_data)

        # -------- Final Status --------
        if result:
            return True

        return False

    except Exception as e:

        print(e)

        speak("Sorry, I couldn't complete your request.")



        return False