import speech_recognition as sr
from voice import speak
import os
from config import STOP,TIMEOUT,PHARSE_TIME_LIMIT,ASSISTANT_NAME
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

         username = os.getlogin()
         speak(f"Hello {username}! How can I help you?")
         print(f"Hello {username}! How can I help you?")

         while True:
            speak("speak your command ")
            print( ASSISTANT_NAME ,": Speak your command ")

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

                print(f"You said : {text}")

                if STOP in text.lower():
                    speak("stop")
                    break

                commands.append(text)
                return text

            except sr.UnknownValueError:
                print( ASSISTANT_NAME ,": Sorry, I could not understand your voice.")
                speak("Sorry, I could not understand your voice.")

            except sr.WaitTimeoutError:
                print(ASSISTANT_NAME ,": No speech detected.")
                speak("No speech detected.")

            except sr.RequestError:
                print(ASSISTANT_NAME ,": Speech recognition service unavailable.")
                speak("Speech recognition service unavailable.")
                return
            
