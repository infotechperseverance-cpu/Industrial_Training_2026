from assistant_state import check_assistant_state
from voice_recognition import speech
from Regsitry import RegistryLauncher,process as registry_process
import os
import assistant_state
from settings import process as settings_process
import asyncio
from voice import speak
from file_folder_management import process as file_process
from reminder import process as reminder_process
from logs import process as logs_process
from config import ASSISTANT_NAME,EXIT_COMMANDS
from search import web_search

launcher = RegistryLauncher()

'''

@Module Name : detect_intent
@Description : This module detects the user's command and performs the
               requested operation.
@Inputparam  : command (User command)
@OutputPara  : None
@Author      : bhoomi sapke

'''

def detect_intent(command):

    command = command.lower().strip()

    if settings_process(command):
        return

    if reminder_process(command):
        return

    if logs_process(command):
        return

    if file_process(command):
        return

    if registry_process(command):
        return

    # Search command
    if command.startswith("search") or "search for" in command:
        web_search(command)
        return
    
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

    username = os.getlogin()
    while True:

        # Sleep mode - wait only for wake word
        while not assistant_state.assistant_active:

            wake_command = speech(language="en-IN")

            if not wake_command:
                continue

            result = assistant_state.check_assistant_state(wake_command)

            if result == "EXIT":
                return

            if result:
                print(f"{username} : {wake_command}")

            

                print(f"{ASSISTANT_NAME}: Hello {username}! How can I help you?")
                asyncio.run(speak(f"Hello {username}! How can I help you?"))

        # Assistant is active
        while assistant_state.assistant_active:

            command = speech()

            if not command:
                continue

            print(f"{username}: {command}")

            # Exit NOVA

            if command.lower() in EXIT_COMMANDS:

                print(f"{ASSISTANT_NAME}: Closing NOVA...")

                asyncio.run(
                    speak("Closing NOVA. Goodbye!")
                )

                os._exit(0)

            # Sleep
            if command.lower() == "go to sleep":
                assistant_state.check_assistant_state(command)
                break

            detect_intent(command)