"""
=========================================
Web Automation Module
Purpose:
Open websites and perform Google searches.
=========================================
"""

import webbrowser
import urllib.parse
import socket
import pywhatkit
from voice_engine import speak
from commandHistory import save_command


# Check Internet Connection
def check_internet():
    try:
        with socket.create_connection(("8.8.8.8", 53), timeout=3):
            return True


    except Exception:
        return False


# Open Google
def open_google():

    if not check_internet():
        speak("Internet connection is unavailable. Please check your network.")
        save_command("Open Google", "Failed")
        return False

    try:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
        save_command("Open Google", "Success")
        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Google.")
        save_command("Open Google", "Failed")
        return False


# Open YouTube
def open_youtube():

    if not check_internet():
        speak("Internet connection is unavailable. Please check your network.")
        save_command("Open YouTube", "Failed")
        return False

    try:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
        save_command("Open YouTube", "Success")
        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open YouTube.")
        save_command("Open YouTube", "Failed")
        return False


# Google Search
def google_search(query):

    if not check_internet():
        speak("Internet connection is unavailable. Please check your network.")
        save_command("Google Search", "Failed")
        return False

    try:
        search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query)

        webbrowser.open(search_url)

        speak(f"Searching Google for {query}.")
        save_command("Google Search", "Success")
        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't complete your search.")
        save_command("Google Search", "Failed")
        return False


# Play Song on YouTube
def play_song(song_name):

    if not check_internet():
        speak("Internet connection is unavailable. Please check your network.")
        save_command("Play Song", "Failed")
        return False

    try:
        pywhatkit.playonyt(song_name)

        speak(f"Playing {song_name} on YouTube.")
        save_command("Play Song", "Success")
        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't play the song.")
        save_command("Play Song", "Failed")
        return False