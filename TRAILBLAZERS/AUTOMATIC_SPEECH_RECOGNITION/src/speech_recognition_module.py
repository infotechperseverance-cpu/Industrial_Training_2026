import speech_recognition as sr
import pyttsx3
import pyaudio
import time
import datetime


recognizer = sr.Recognizer()

engine = pyttsx3.init()


def initialize_voice():
    voices = engine.getProperty('voices')

    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)


def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print("Voice output error")


def check_microphone():
    try:
        mic_list = sr.Microphone.list_microphone_names()
        if len(mic_list) == 0:
            print("No microphone found")
            speak("No microphone found")
            return False
        return True
    except:
        print("Microphone error")
        return False


def listen():
    if not check_microphone():
        return None

    try:
        with sr.Microphone() as source:
            print("\nAdjusting for noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Listening... Speak now")
            speak("I am listening")

            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

    except sr.WaitTimeoutError:
        print("No speech detected")
        speak("No speech detected")
        return None

    except Exception as e:
        print("Microphone error:", e)
        speak("Microphone error")
        return None


    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        text = text.lower()
        save_log(text)

        print("\nYou said:", text)
        return text

    except sr.UnknownValueError:
        print("Could not understand audio")
        speak("Sorry, I could not understand")
        return None

    except sr.RequestError:
        print("Internet error")
        speak("Please check your internet connection")
        return None

    except Exception as e:
        print("Error:", e)
        speak("Speech recognition error")
        return None

def save_log(text):

    try:

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("voice_log.txt", "a") as file:

            file.write(f"{time} - {text}\n")

    except Exception:

        print("Logging failed")


def main():
    initialize_voice()

    print("=" * 40)
    print("VOICE INPUT MODULE STARTED")
    print("=" * 40)

    while True:
        text = listen()

        if text:
            speak("You said " + text)

        print("\nPress ENTER to speak again or type exit to stop")
        choice = input().lower()

        if choice == "exit":
            speak("Goodbye")
            break


if __name__ == "__main__":
    main()
