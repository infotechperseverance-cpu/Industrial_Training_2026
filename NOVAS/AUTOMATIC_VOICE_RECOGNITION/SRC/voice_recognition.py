'''
@Module Name : voice_recognition.py

@Description : This module captures voice input from the
               microphone, converts it into text using
               Google Speech Recognition, and returns the
               recognized command.

@InputParam  : None

@OutputParam : Recognized text / None

@Author      : Vaishnavi Teli
'''

import asyncio
import time

import speech_recognition as sr

from logs import add_log
from voice import speak
from config import (
    TIMEOUT,
    PHRASE_TIME_LIMIT,
    DEFAULT_SPEECH_LANGUAGE
)

# Create recognizer object
recognizer = sr.Recognizer()

# Store recognized commands
commands = []


'''
@Function Name : speech

@Description   : Captures voice input from the microphone,
                 converts it into text using Google Speech
                 Recognition and returns the recognized text.

@InputParam    : language

@OutputParam   : Recognized text / None

@Author        : Vaishnavi Teli
'''
def speech(language=DEFAULT_SPEECH_LANGUAGE):

    time.sleep(0.8)

    try:

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=TIMEOUT,
                phrase_time_limit=PHRASE_TIME_LIMIT
            )

            try:

                text = recognizer.recognize_google(
                    audio,
                    language=language
                )

                text = text.lower().strip()

                commands.append(text)

                # Save success log
                try:

                    add_log(
                        module="Voice Recognition",
                        command=text,
                        status="SUCCESS"
                    )

                except Exception as e:

                    print(f"Log Error: {e}")

                return text

            except sr.UnknownValueError:

                try:

                    add_log(
                        module="Voice Recognition",
                        command="Unknown Speech",
                        status="FAILED"
                    )

                except Exception as e:

                    print(f"Log Error: {e}")

                return None

            except sr.RequestError as e:

                asyncio.run(
                    speak(f"Google Speech API Error: {e}")
                )

                return None

    except sr.WaitTimeoutError:

        asyncio.run(
            speak("No speech detected.")
        )

        return None

    except OSError as e:

        asyncio.run(
            speak(f"Microphone Error: {e}")
        )

        return None

    except Exception as e:

        asyncio.run(
            speak(f"Speech Recognition Error: {e}")
        )

        return None