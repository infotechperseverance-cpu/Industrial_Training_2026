from assistant_state import check_assistant_state
from voice_recognition import speech
from Regsitry import RegistryLauncher
from voice import speak
import os
import assistant_state

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

    command = command.lower()

    if command.startswith("open"):
        launcher.launch(command)

    elif "file" in command or "folder" in command:
       pass

    elif "email" in command:
        pass

    elif "system" in command:
        pass

    else:
        speak("Command not recognized.")

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

                print(f"You said : {wake_command}")

                username = os.getlogin()

                print(f"Hello {username}! How can I help you?")
                speak(f"Hello {username}! How can I help you?")

        # Assistant is active
        while assistant_state.assistant_active:

            command = speech()

            if not command:
                continue

            print(f"You said : {command}")

            # Exit
            if command.lower() == "exit":
                speak("Closing NOVA.")
                return

            # Sleep
            if command.lower() == "go to sleep":
                assistant_state.check_assistant_state(command)
                break

            detect_intent(command)