"""
=========================================
Voice Engine Module
Purpose:
Convert text to speech.
=========================================
"""

import pyttsx3
from config import VOICE_RATE, VOICE_VOLUME

engine = pyttsx3.init()


engine.setProperty("rate", VOICE_RATE)
engine.setProperty("volume", VOICE_VOLUME)

# Select Female Voice
voices = engine.getProperty("voices")

for voice in voices:
    if "zira" in voice.name.lower():
        engine.setProperty("voice", voice.id)

        break
else:
    # If Zira is not found, use the second installed voice (usually female)
    if len(voices) > 1:
        engine.setProperty("voice", voices[1].id)


def speak(text):
    try:
        engine.stop()
        if text:
            engine.say(str(text))
            engine.runAndWait()
    except Exception as e:
        print("Voice Error:", e)