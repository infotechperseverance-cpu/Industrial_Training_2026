from config import *
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

    if any(word in command for word in WAKE_WORDS):
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