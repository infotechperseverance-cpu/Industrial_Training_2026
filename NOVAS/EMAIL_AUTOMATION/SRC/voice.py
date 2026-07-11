from gtts import gTTS
from playsound import playsound
import os
import uuid
import threading

voice_lock = threading.Lock()

def speak(text):
    

    with voice_lock:

        filename = f"voice_{uuid.uuid4().hex}.mp3"

        try:
            tts = gTTS(text=text, lang="en")
            tts.save(filename)
            playsound(filename)

        finally:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except PermissionError:
                    pass