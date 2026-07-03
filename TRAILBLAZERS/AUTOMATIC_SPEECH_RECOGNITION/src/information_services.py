import speech_recognition as sr
import win32com.client
import webbrowser
from datetime import datetime

#--------Text-to-Speech-------
speaker = win32com.client.Dispatch("SAPI.SpVoice")
def speak(text):
    print(text)
    speaker.Speak(text)

#----------Voice Input------------
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        speak("Listening")

        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source,timeout = 10,phrase_time_limit = 10)
        
    try:
        command = recognizer.recognize_google(audio,language = "en-IN")
        speak("You said "+ command)
        return command.lower()
    
    except sr.UnknownValueError:
        speak("please speak again")
        return listen()
    
    except:
        speak("I could not understand")
        return "" 

def Information_services(command):

    if "time" in command:
        current_time = datetime.now().strftime("%I;%M %p")
        speak("current time is"  +current_time)   

    elif "date" in command:
        current_date = datetime.now().strftime("%d-%m-%Y")
        speak("Today's date is "+current_date)


    elif "google" in command:
        speak("opening google")
        webbrowser.open("https://www.google.com")

speak("Say your command")
command = listen()

Information_services(command)


            
