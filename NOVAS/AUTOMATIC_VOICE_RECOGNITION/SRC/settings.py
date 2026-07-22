'''
@Module Name : settings.py

@Description : This module manages the NOVA settings menu.
               It allows the user to change language, voice,
               screen brightness, and shutdown options through
               voice commands.

@InputParam  : Voice commands

@OutputParam : Executes the selected settings operation

@Author      : Vaishnavi Teli
'''

import asyncio
import time

from voice import speak
from voice_customization import select_voice
from laptop_setting import brightness, shutdown
from voice_setting import get_settings
from config import SETTINGS_TEXT,EXIT_COMMANDS


def open_settings():

    while True:

        try:
            settings = get_settings()
            speech_lang = settings["speech"]

            text = SETTINGS_TEXT.get(
                speech_lang,
                SETTINGS_TEXT["en-IN"]
            )

            asyncio.run(speak(text["opening"]))

            print(text["menu"])

            asyncio.run(speak(text["prompt"]))

            from voice_recognition import speech

            time.sleep(1)

            command = speech()

            if not command:
                return

            command = command.lower().strip()

            if (
                "change language and voice" in command
                or "language and voice" in command
                or "change language" in command
                or "change voice" in command
            ):
                select_voice()
                continue

            elif "brightness" in command:
                brightness(command)

            elif "shutdown" in command:
                shutdown()

            elif EXIT_COMMANDS in command:
                return

            else:
                asyncio.run(speak(text["invalid"]))

        except Exception as e:

            print(f"Settings Error: {e}")

            asyncio.run(
                speak("Unable to open settings.")
            )

            return
        
'''
@Function Name : process
@Description   : Processes settings-related commands.
@Input Param   : command
@Output Param  : TRUE if command is handled, otherwise FALSE.
@Author        : Bhoomi Sapke
'''

def process(command):

    command = command.lower().strip()

    keywords = [
        "setting",
        "settings",
        "open settings",
        "system settings"
    ]

    for keyword in keywords:
        if keyword in command:
            open_settings()
            return True

    return False