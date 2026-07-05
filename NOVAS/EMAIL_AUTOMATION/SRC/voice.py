from gtts import gTTS
from playsound import playsound
import os

def speak(text):
    print(text)

    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"

    tts.save(filename)
    playsound(filename)

    os.remove(filename)