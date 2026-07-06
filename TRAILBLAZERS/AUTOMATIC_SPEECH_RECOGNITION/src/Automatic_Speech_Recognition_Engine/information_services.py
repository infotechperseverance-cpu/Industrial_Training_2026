"""
=========================================
Information Services Module
Purpose:
Provide basic information to the user.
=========================================
"""

from datetime import datetime
from voice_engine import speak
from commandHistory import save_command


# Get Current Time
def current_time():
    try:
        current_time = datetime.now().strftime("%I:%M %p")

        print("Current Time :", current_time)
        speak("The current time is " + current_time)

        save_command("Current Time", "Success")
        return current_time

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't get the current time.")
        save_command("Current Time", "Failed")
        return None


# Get Current Date
def current_date():
    try:
        current_date = datetime.now().strftime("%d %B %Y")

        print("Today's Date :", current_date)
        speak("Today is " + current_date)

        save_command("Current Date", "Success")
        return current_date

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't get today's date.")
        save_command("Current Date", "Failed")
        return None


# Get Current Day
def current_day():
    try:
        current_day = datetime.now().strftime("%A")

        print("Today :", current_day)
        speak("Today is " + current_day)

        save_command("Current Day", "Success")
        return current_day

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't get today's day.")
        save_command("Current Day", "Failed")
        return None

# Hello Assistant
def hello_assistant():
    speak("Hello! How can I help you today?")
    save_command("Hello Assistant", "Success")
    return True


def good_morning():
    speak("Good morning! Have a great day.")
    save_command("Good Morning", "Success")
    return True


def good_afternoon():
    speak("Good afternoon! How may I assist you?")
    save_command("Good Afternoon", "Success")
    return True


def good_evening():
    speak("Good evening! How can I help you?")
    save_command("Good Evening", "Success")
    return True


def how_are_you():
    speak("I am doing great. Thank you for asking.")
    save_command("How Are You", "Success")
    return True


def assistant_name():
    speak("I am your Smart Voice Assistant.")
    save_command("Assistant Name", "Success")
    return True