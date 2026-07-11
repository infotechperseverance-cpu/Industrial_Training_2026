"""
=========================================
Voice Engine Module
Purpose:
Convert text to speech.
=========================================
"""

import threading
import pyttsx3

engine = pyttsx3.init("sapi5")
engine_lock = threading.Lock()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")

# Force Zira
engine.setProperty("voice", voices[1].id)

print("Using voice:", voices[1].name)


def speak(text):
    if not text:
        return

    with engine_lock:
        engine.say(str(text))
        engine.runAndWait()