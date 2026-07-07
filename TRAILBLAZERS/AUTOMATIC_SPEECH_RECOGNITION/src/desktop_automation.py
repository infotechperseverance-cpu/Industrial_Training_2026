"""
=========================================
Desktop Automation Module
Purpose:
Open desktop applications using voice commands.
=========================================
"""

import os
import subprocess
import pyautogui
from datetime import datetime
from voice_engine import speak
from commandHistory import save_command


# Open Calculator
def open_calculator():
    try:
        subprocess.Popen("calc")
        speak("Calculator has been opened.")

        return True


    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Calculator.")

        return False


# Open Notepad
def open_notepad():
    try:
        subprocess.Popen("notepad")
        print("Notepad has been opened.")
        return True

    except Exception as e:
        print(e)
        print("Sorry, I couldn't open Notepad.")
        return False


# Open Google Chrome
def open_chrome():
    try:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

        if os.path.exists(chrome_path):
            subprocess.Popen(chrome_path)
            speak("Opening Chrome.")

            return True

        speak("Chrome is not installed.")

        return False

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Chrome.")

        return False


# Open File Explorer
def open_file_explorer():
    try:
        subprocess.Popen("explorer")
        speak("File Explorer has been opened.")

        return True

    except Exception as e :
        print(e)
        speak("Sorry, I couldn't open File Explorer.")

        return False


# Open Downloads Folder
def open_downloads():
    try:
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        os.startfile(downloads)
        speak("Opening Downloads folder.")

        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Downloads.")

        return False


# Open Documents Folder
def open_documents():
    try:
        documents = os.path.join(os.path.expanduser("~"), "Documents")
        os.startfile(documents)
        speak("Opening Documents folder.")

        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Documents.")

        return False

# Shutdown Computer
def shutdown_computer():

    try:

        os.system("shutdown /s /t 0")

        save_command("Shutdown Computer", "Success")

        return True

    except Exception as e:

        print(e)

        speak("Sorry, I couldn't shut down the computer.")
        return False

# Restart Computer
def restart_computer():

    try:

        os.system("shutdown /r /t 0")
        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't restart the computer.")
        return False


# Lock Computer
def lock_computer():

    try:

        os.system("rundll32.exe user32.dll,LockWorkStation")

        speak("Your computer is being locked.")

        return True

    except Exception as e:

        print(e)

        speak("Sorry, I couldn't lock the computer.")

        return False




def open_vscode():

    paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"
    ]

    for path in paths:
        if os.path.exists(path):
            subprocess.Popen([path])
            speak("Opening Visual Studio Code.")

            return True

    speak("Visual Studio Code is not installed.")

    return False

def take_screenshot():
    try:
        filename = datetime.now().strftime("Screenshot_%Y%m%d_%H%M%S.png")
        image = pyautogui.screenshot()
        image.save(filename)

        speak("Screenshot captured successfully.")

        return True

    except Exception as e:
        print(e)
        speak("Unable to capture screenshot.")

        return False

def increase_volume():
    try:
        pyautogui.press("volumeup")
        speak("Volume increased.")

        return True

    except Exception as e:
        print(e)

        return False

def decrease_volume():
    try:
        pyautogui.press("volumedown")
        speak("Volume decreased.")

        return True

    except Exception as e:
        print(e)

        return False

def mute_volume():
    try:
        pyautogui.press("volumemute")
        speak("Volume muted.")

        return True

    except Exception as e:
        print(e)
        return False

def unmute_volume():
    return mute_volume()