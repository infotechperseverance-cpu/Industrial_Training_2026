import speech_recognition as sr
import win32com.client
import webbrowser
from datetime import datetime
import os
import json

#------------JSON command------------
with open("commands.json", "r")as file:
     commands = json.load(file)
     
#--------Text-to-Speech-------
speaker = win32com.client.Dispatch("SAPI.SpVoice")
def speak(text):
    print(text)
    speaker.Speak(text)

#----------Voice Input------------
def voice_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        speak("Listening")

        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source,timeout = 10,phrase_time_limit = 10)
        
    try:
        command = recognizer.recognize_google(audio,language = "en-IN")
        command = command.lower().strip()
        print("You said :", command)
        return command
    
    except sr.UnknownValueError:
        speak("I could not understand")
        return None
    
    except sr.RequestError:
        speak("Internet error")
        return None
    
#------------------process command-----------------    
def process_command(command):

    if command is None:
        return True
    
    action = commands.get(command)

    if action =="chrome":
         speak("open chrome successfully")
         webbrowser.open("https://www.google.com")

    elif action == "calculator":
            speak("open calculator successfully")
            os.system("calc")
                    
    elif action =="notepad":
            speak("open notepad successfully")
            os.system("notepad")

    elif action == "explorer":
            speak(" open file_explorer successfully")
            os.system("explorer")            

    elif action =="downloads":
            speak("open downloads successfully")
            os.startfile(os.path.expanduser("`/Downloads"))
           
    elif action =="documents":
            speak("open documents successfully")
            os.startfile(os.path.expanduser("~/Documents"))   

    elif action == "time":
        current_time = datetime.now().strftime("%I:%M %p")
        print(current_time)
        speak("current time is"  +current_time)   

    elif action =="date":
        current_date = datetime.now().strftime("%d-%m-%Y")
        print(current_date)
        speak("Today's date is "+current_date)

    elif action == "exit":
         speak("goodbye")
         return False

    else:
         speak("unsupported command")

    return True

#-------------Main program------------
while True:
     
     command = voice_command()

     if not process_command(command):
          break
    