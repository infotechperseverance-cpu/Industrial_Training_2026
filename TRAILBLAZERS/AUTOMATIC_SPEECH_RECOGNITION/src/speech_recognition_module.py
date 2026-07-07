import speech_recognition as sr
import time
import datetime
from voice_engine import speak
from config import (
    VOICE_LOG_FILE,
    LISTEN_TIMEOUT,
    PHRASE_TIME_LIMIT,
    AMBIENT_NOISE_DURATION,
)
recognizer = sr.Recognizer()
recognizer.energy_threshold = 120
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.2
recognizer.non_speaking_duration = 0.3
recognizer.operation_timeout = None

def check_microphone():
    try:
        mic_list = sr.Microphone.list_microphone_names()
        if len(mic_list) == 0:
            print("No microphone found")
            speak("No microphone found")
            return False
        return True

    except Exception as e:
        print(e)
        speak("Microphone error")
        return False


def listen():


    if not check_microphone():
        return None

    try:

        with sr.Microphone() as source:

            print("\nAdjusting for noise...")
            recognizer.adjust_for_ambient_noise(source, duration=AMBIENT_NOISE_DURATION)
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 1.0
            recognizer.phrase_threshold = 0.3
            recognizer.non_speaking_duration = 0.5


            print("Listening... Speak now")
            speak("Listening... Speak now")
            time.sleep(0.4)
            audio = recognizer.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_TIME_LIMIT,snowboy_configuration=None)

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

        text = None

        # Try Indian English first
        try:
            text = recognizer.recognize_google(audio, language="en-IN")
        except sr.UnknownValueError:
            pass

        # If it failed, try US English
        if text is None:
            try:
                text = recognizer.recognize_google(audio, language="en-US")
            except sr.UnknownValueError:
                pass

        # If both failed
        if text is None:
            print("Could not understand audio")
            speak("Sorry, I could not understand.")
            return None

        text = text.strip()  # Remove leading/trailing spaces
        text = text.lower()  # Convert to lowercase

        save_log(text)

        print("\nYou said:", text)

        return text

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

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(VOICE_LOG_FILE, "a") as file:

            file.write(f"{current_time} - {text}\n")

    except Exception:

        print("Logging failed")

# ---------------- Start Listening ----------------

def start_listening():
    speak("I'm listening. Please tell me your command.")
    return True


# ---------------- Stop Listening ----------------

def stop_listening():
    speak("Voice recognition has been stopped.")
    return True

