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
        save_command("Open Calculator", "Success")
        return True


    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Calculator.")
        save_command("Open Calculator", "Failed")
        return False


# Open Notepad
def open_notepad():
    try:
        subprocess.Popen("notepad")
        speak("Notepad has been opened.")
        save_command("Open Notepad", "Success")
        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Notepad.")
        save_command("Open Notepad", "Failed")
        return False


# Open Google Chrome
def open_chrome():
    try:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

        if os.path.exists(chrome_path):
            subprocess.Popen(chrome_path)
            speak("Opening Chrome.")
            save_command("Open Chrome", "Success")
            return True

        speak("Chrome is not installed.")
        save_command("Open Chrome", "Failed")
        return False

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Chrome.")
        save_command("Open Chrome", "Failed")
        return False


# Open File Explorer
def open_file_explorer():
    try:
        subprocess.Popen("explorer")
        speak("File Explorer has been opened.")
        save_command("Open File Explorer", "Success")
        return True

    except Exception as e :
        print(e)
        speak("Sorry, I couldn't open File Explorer.")
        save_command("Open File Explorer", "Failed")
        return False


# Open Downloads Folder
def open_downloads():
    try:
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        os.startfile(downloads)
        speak("Opening Downloads folder.")
        save_command("Open Downloads", "Success")
        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Downloads.")
        save_command("Open Downloads", "Failed")
        return False


# Open Documents Folder
def open_documents():
    try:
        documents = os.path.join(os.path.expanduser("~"), "Documents")
        os.startfile(documents)
        speak("Opening Documents folder.")
        save_command("Open Documents", "Success")
        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Documents.")
        save_command("Open Documents", "Failed")
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

        save_command("Shutdown Computer", "Failed")

        return False

# Restart Computer
def restart_computer():

    try:

        os.system("shutdown /r /t 0")

        save_command("Restart Computer", "Success")

        return True

    except Exception as e:

        print(e)

        speak("Sorry, I couldn't restart the computer.")

        save_command("Restart Computer", "Failed")

        return False


# Lock Computer
def lock_computer():

    try:

        os.system("rundll32.exe user32.dll,LockWorkStation")

        speak("Your computer is being locked.")

        save_command("Lock Computer", "Success")

        return True

    except Exception as e:

        print(e)

        speak("Sorry, I couldn't lock the computer.")

        save_command("Lock Computer", "Failed")

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
            save_command("Open VS Code", "Success")
            return True

    speak("Visual Studio Code is not installed.")
    save_command("Open VS Code", "Failed")
    return False

def take_screenshot():
    try:
        filename = datetime.now().strftime("Screenshot_%Y%m%d_%H%M%S.png")
        image = pyautogui.screenshot()
        image.save(filename)

        speak("Screenshot captured successfully.")
        save_command("Take Screenshot", "Success")
        return True

    except Exception as e:
        print(e)
        speak("Unable to capture screenshot.")
        save_command("Take Screenshot", "Failed")
        return False

def increase_volume():
    try:
        pyautogui.press("volumeup")
        speak("Volume increased.")
        save_command("Increase Volume", "Success")
        return True

    except Exception as e:
        print(e)
        save_command("Increase Volume", "Failed")
        return False

def decrease_volume():
    try:
        pyautogui.press("volumedown")
        speak("Volume decreased.")
        save_command("Decrease Volume", "Success")
        return True

    except Exception as e:
        print(e)
        save_command("Decrease Volume", "Failed")
        return False

def mute_volume():
    try:
        pyautogui.press("volumemute")
        speak("Volume muted.")
        save_command("Mute Volume", "Success")
        return True

    except Exception as e:
        print(e)
        save_command("Mute Volume", "Failed")
        return False

def unmute_volume():
    return mute_volume()