
'''

@Module Name : voice_recognition.py
@Description : Voice Input Recognition Module
@InputParam  : None
@OutputParam : None
@Author      : Vaishnavi Teli

'''

import speech_recognition as sr
import asyncio

from config import (
    TIMEOUT,
    PHARSE_TIME_LIMIT,
    DEFAULT_SPEECH_LANGUAGE
)

from voice_setting import get_settings
from voice import speak
from logs import add_log


# Create recognizer object
recognizer = sr.Recognizer()

# Store commands
commands = []


def speech(language=None):

    # Get saved voice settings
    settings = get_settings()

    # Use selected language
    if language is None:
        language = settings.get(
            "speech",
            DEFAULT_SPEECH_LANGUAGE
        )


    try:

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=2
            )

            audio = recognizer.listen(
                source,
                timeout=TIMEOUT,
                phrase_time_limit=PHARSE_TIME_LIMIT
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

                    print("Log Error:", e)


                return text



            except sr.UnknownValueError:

                asyncio.run(
                   speak(  "❌ Google could not understand speech")
                 )


                try:

                    add_log(
                        module="Voice Recognition",
                        command="Unknown Speech",
                        status="FAILED"
                    )

                except Exception as e:
                    return None

                return None



            except sr.RequestError as e:

                asyncio.run(
                   speak(  "❌ Google Speech API Error:",
                    e)
                 )

                return None



    except sr.WaitTimeoutError:

        asyncio.run(
            speak(  "No Detect speech"
               )
            )

        try:

            asyncio.run(
                speak(
                    "No speech detected"
                )
            )

        except Exception:
            pass


        return None



    except OSError as e:

           print(
            "Microphone Error:",
            e
          )



    except Exception as e:

        print(
            "Speech Recognition Error:",
            e
        )

    
    
    
