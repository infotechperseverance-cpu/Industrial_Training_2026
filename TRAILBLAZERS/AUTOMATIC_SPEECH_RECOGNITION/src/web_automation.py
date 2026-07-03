import speech_recognition as sr
import pyttsx3
import webbrowser
import urllib.parse
import socket
import time

# ---------------------- Text To Speech ----------------------

engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)   # Female Voice


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# ---------------------- Internet Check ----------------------

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False

# ---------------------- Play Song ----------------------

def play_song(song_name):

    search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(song_name)

    webbrowser.open(search_url)

    time.sleep(2)

    speak(f"Playing {song_name} on YouTube.")
# ---------------------- Voice Input ----------------------

recognizer = sr.Recognizer()

def take_command():

    with sr.Microphone() as source:

        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

            command = recognizer.recognize_google(audio)
            command = command.lower()

            print("You:", command)
            return command

        except sr.UnknownValueError:
            speak("Sorry, I could not understand.")
            return ""

        except sr.RequestError:
            speak("Speech Recognition service is unavailable.")
            return ""

        except sr.WaitTimeoutError:
            return ""

        except Exception:
            speak("Something went wrong.")
            return ""


# ---------------------- Open Google ----------------------

def open_google():
    webbrowser.open("https://www.google.com")
    time.sleep(2)
    speak("Google opened successfully.")


# ---------------------- Open YouTube ----------------------

def open_youtube():
    webbrowser.open("https://www.youtube.com")
    time.sleep(2)
    speak("YouTube opened successfully.")


# ---------------------- Google Search ----------------------

def google_search(query):

    search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query)

    webbrowser.open(search_url)

    time.sleep(2)

    speak(f"Searching Google for {query}")


# ---------------------- Main ----------------------

def main():

    speak("Web Automation Module Started.")

    if not check_internet():
        speak("Internet connection is unavailable.")
        return

    while True:

        command = take_command()

        if command == "":
            continue

        if "open google" in command:
            open_google()

        elif "open youtube" in command:
            open_youtube()

        elif "search" in command:

            query = command.replace("search", "").strip()

            if query:
                google_search(query)
            else:
                speak("Please tell me what you want to search.")

        # Play Song
        elif "play" in command:

            song = command.replace("play", "").strip()

            if song:
                play_song(song)
            else:
                speak("Please tell me the song name.")

        elif command == "stop" or command == "exit":
            speak("Stopping Web Automation. Goodbye.")
            break

        else:
            speak("Sorry, I don't know this command.")


# ---------------------- Run ----------------------

if __name__ == "__main__":
    main()