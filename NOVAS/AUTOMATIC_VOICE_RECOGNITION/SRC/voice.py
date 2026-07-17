"""

@Module Name : voice.py
@Description : Convert text to speech using the 
               selected Edge-TTS voice.
@Author      : Vaishani Teli

"""

import edge_tts
from playsound import playsound
import os
from voice_setting import get_settings


async def speak(text, voice=None):

    settings = get_settings()

    if voice is None:
        voice = settings["voice"]

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    filename = "voice.mp3"

    await communicate.save(filename)

    playsound(filename)

    if os.path.exists(filename):
        os.remove(filename)