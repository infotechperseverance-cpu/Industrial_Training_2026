import speech_recognition as sr
from voice import speak
import os
from config import TIMEOUT,PHARSE_TIME_LIMIT,ASSISTANT_NAME
from website import open_website
recognizer = sr.Recognizer()
commands = []

'''

@Module Name : speech
@Description : This module take a command from user 
@InputParam  : NONE
@OutputParam : NONE
@Author      : Vainshnavi Teli

'''

def speech():

    with sr.Microphone() as source:
         
         recognizer.adjust_for_ambient_noise(source, duration=1)

         while True:

            try:
                audio = recognizer.listen(
                    source,
                    TIMEOUT,
                    PHARSE_TIME_LIMIT
                )

                text = recognizer.recognize_google(
                    audio,
                    language="en-IN"
                ).strip()

                commands.append(text)
                return text

            except sr.UnknownValueError:
                return None
            
            except sr.WaitTimeoutError:
                print(ASSISTANT_NAME ,": No speech detected.")
                speak("No speech detected.")

            except sr.RequestError:
                print(ASSISTANT_NAME ,": Speech recognition service unavailable.")
                speak("Speech recognition service unavailable.")
                return           