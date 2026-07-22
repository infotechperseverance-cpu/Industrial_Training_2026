"""
@Module Name : voice.py

@Description : This module converts text into speech using
               the selected Edge-TTS voice and plays the
               generated audio.

@InputParam  : Text to speak, Voice (Optional)

@OutputParam : Voice Output

@Author      : Vaishnavi Teli
"""

import os
import uuid
import threading

import edge_tts
from playsound import playsound

from voice_setting import get_settings


# Prevent multiple threads from speaking simultaneously
speech_lock = threading.Lock()


'''
@Function Name : speak

@Description   : Converts the given text into speech using
                 Microsoft Edge-TTS and plays the generated
                 audio.

@InputParam    : text, voice (Optional)

@OutputParam   : Voice Output

@Author        : Vaishnavi Teli
'''
async def speak(text, voice=None):

    settings = get_settings()

    if voice is None:
        voice = settings["voice"]

    with speech_lock:

        filename = f"voice_{uuid.uuid4().hex}.mp3"

        try:

            communicate = edge_tts.Communicate(
                text=text,
                voice=voice
            )

            await communicate.save(filename)

            playsound(filename)

        except Exception as e:

            print(f"Voice Error: {e}")

        finally:

            if os.path.exists(filename):

                try:
                    os.remove(filename)

                except PermissionError:
                    pass