from assistant_state import check_assistant_state
from voice_recognition import speech
from Regsitry import RegistryLauncher
import os
import assistant_state
from settings import open_settings
import asyncio
from voice import speak
from file_folder_management import process

launcher = RegistryLauncher()

'''

@Module Name : detect_intent
@Description : This module detects the user's command and performs the
               requested operation.
@Inputparam  : command (User command)
@OutputPara  : None
@Author      : Vaishnavi Teli

'''

def detect_intent(command):

    command = command.lower().strip()


    # Open settings
    if "setting" in command:
        open_settings()


    # Open files/folders/process
    elif "file" in command or "folder" in command:
        process(command)

    elif "remainder" in command:
        pass

    elif "view logs" in command or "log" in command:
        pass

    # Open applications
    elif command.startswith("open"):
        launcher.launch(command)


    else:
        asyncio.run(
            speak("Command not recognized.")
        )

        

'''

@Function Name : process_command
@Description   : This function continuously listens for the wake word.
                 When the assistant is activated, it listens for the
                 user's command and sends it to the intent detection module.
@Inputparam    : None
@OutputPara    : None
@Author        : Vaishnavi Teli

'''
def process_command():

    while True:

        # Sleep mode - wait only for wake word
        while not assistant_state.assistant_active:

            wake_command = speech()

            if not wake_command:
                continue

            result = assistant_state.check_assistant_state(wake_command)

            if result == "EXIT":
                return

            if result:

                print(f"{username} : {wake_command}")

                username = os.getlogin()

                print(f"Hello {username}! How can I help you?")
                asyncio.run(speak(f"Hello {username}! How can I help you?"))

        # Assistant is active
        while assistant_state.assistant_active:

            command = speech()

            if not command:
                continue

            print(f"{username}: {command}")

            # Exit
            if command.lower() == "exit":
                asyncio.run(speak("Closing NOVA."))
                return

            # Sleep
            if command.lower() == "go to sleep":
                assistant_state.check_assistant_state(command)
                break

            detect_intent(command)