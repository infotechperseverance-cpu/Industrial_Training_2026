import os
import subprocess
import speech_recognition as sr
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")
def speak(text):
    print(text)
    speaker.Speak(text)

def open_calculator():
    os.system("calc")

def open_notepad():
    os.system("notepad")

def open_chrome():
     chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
     if os.path.exists(chrome_path):
        subprocess.Popen(chrome_path)
     else:
        print("Chrome is not installed.")

def open_file_explorer():
    os.system("explorer")

def open_downloads():
    downloads = os.path.join(os.path.expanduser("~"),"Downloads")
    os.startfile(downloads)

def open_documents():
    documents = os.path.join(os.path.expanduser("~"),"Documents")
    os.startfile(documents)



# ----------------- Speech Recognition -----------------
def voice_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        speak("Listening")
        print("\nSpeak your command...")

        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        speak("You said "+command)
        

        if "calculator" in command:
            open_calculator()
            speak("calculator open successfully")
           
            
        elif "notepad" in command:
            open_notepad()
            speak("notepad open successfully")
           

        elif "chrome" in command:
            open_chrome()
            speak("chrome open successfully")
            

        elif "explorer" in command or "file explorer" in command:
            open_file_explorer()
            speak("explorer open successfully")
            

        elif "downloads" in command:
            open_downloads()
            speak("downloads open successfully")
           
        elif "document" in command:
            open_documents()
            speak("documents open successfully")
            
        elif "exit" in command: 
            speak("Goodbay")
            exit() 
        
        else:
            speak("I don't understand this command")

    except sr.UnknownValueError:
        print("Could not understand your voice.")
        speak("Could not understand your voice")

    except sr.RequestError:
        print("Speech Recognition service unavailable.")
        speak("Speech Recongnition service unavailable")
# ----------------- Main Menu -----------------    

while True:

    print("==========Desktop Automation=============")
    print("1.Open Calculator")
    print("2.Open Notepad")
    print("3.Open Chrome")
    print("4.Open File Explorer")
    print("5.Open Downlods")
    print("6.Open Document")
    print("7.Voice Command")
    print("8.Open Exit")

    choice = input("Enter your Choice: ")

    if choice == "1":
        open_calculator()
        print("Calulater open successfully")

    elif choice =="2":
        open_notepad()
        print("Notepad open successfully")

    elif choice =="3":
        open_chrome()
        print("chrome open successfully")    
    
    elif choice =="4":
        open_file_explorer()
        print("file explorer open successfully")  

    elif choice =="5":
        open_downloads()
        print("downloads open successfully")

    elif choice =="6":
        open_documents()
        print("document open successfully")   

    elif choice =="7":
        voice_command()

    elif choice =="8":
        print("Exit desktop successfully") 
        break   

    else:
        print("Invalid choice! Please try again.")
       






    




