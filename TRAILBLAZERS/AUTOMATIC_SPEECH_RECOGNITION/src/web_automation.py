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

        return False

    try:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")

        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open Google.")

        return False


# Open YouTube
def open_youtube():

    if not check_internet():
        speak("Internet connection is unavailable. Please check your network.")

        return False

    try:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't open YouTube.")

        return False


# Google Search
def google_search(query):

    if not check_internet():
        speak("Internet connection is unavailable. Please check your network.")

        return False

    try:
        search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query)

        webbrowser.open(search_url)

        speak(f"Searching Google for {query}.")

        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't complete your search.")

        return False


# Play Song on YouTube
def play_song(song_name):

    if not check_internet():
        speak("Internet connection is unavailable. Please check your network.")

        return False

    try:
        pywhatkit.playonyt(song_name)

        speak(f"Playing {song_name} on YouTube.")

        return True

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't play the song.")

        return False