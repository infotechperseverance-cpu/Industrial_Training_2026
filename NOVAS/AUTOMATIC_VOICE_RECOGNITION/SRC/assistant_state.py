'''
@Module Name : assistant_state.py

@Description : Manages the current state of the NOVA assistant.
               It handles wake, sleep and exit commands.

@InputParam  : User voice command

@OutputParam : Assistant state

@Author      : Bhoomi Sapke
'''


from config import (
    WAKE_RESPONSE,
    SLEEP_COMMAND,
    SLEEP_RESPONSE,
    EXIT_COMMAND,
    ASSISTANT_NAME
)
from voice import speak
import asyncio

WAKE_WORDS = [
    "hi nova",
    "hey nova",
    "hello nova",
    "hi novas",
    "hey novas",
    "hello novas",
    "hello nov"
]

assistant_active = False

def check_assistant_state(command):

    global assistant_active

    command = command.lower()

    if command in WAKE_WORDS:
        assistant_active = True
        asyncio.run(speak(WAKE_RESPONSE))
        return True

    elif SLEEP_COMMAND.lower() in command:
        assistant_active = False
        asyncio.run(speak(SLEEP_RESPONSE))
        return True

    elif EXIT_COMMAND.lower() in command:
        asyncio.run(speak(f"Closing {ASSISTANT_NAME}."))
        return "EXIT"

    return False