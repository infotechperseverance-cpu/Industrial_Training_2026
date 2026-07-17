"""
@Module Name : voice_customization.py
@Description : Language and Voice Selection Module
@Author      : Vaishnavi Teli

"""

import asyncio
import time
from config import (
    VOICE_OPTIONS,
    NUMBER_WORDS,
    LANGUAGE_ALIASES,
    SAMPLE_TEXT,
    YES_WORDS,
    NO_WORDS
)
from voice_setting import save_voice

FILE_NAME = "voice_data.json"

'''

@Function Name : word_to_number
@Description   : Converts a spoken number into its numeric value.
@InputParam    : text (String)
@OutputParam   : Number or None

'''

def word_to_number(text):

    if not text:
        return None

    text = text.lower().strip()

    for number, words in NUMBER_WORDS.items():
        if text in words:
            return number

    return None

'''

@Function Name : get_language_choice
@Description   : Identifies the selected language from the user's spoken
                 command.
@InputParam    : command (String), languages (List)
@OutputParam   : Language number or None

'''

def get_language_choice(command, languages):

    if not command:
        return None

    command = command.lower().strip()

    # Check language aliases
    if command in LANGUAGE_ALIASES:
        language = LANGUAGE_ALIASES[command]

        if language in languages:
            return languages.index(language) + 1

    # Check number words
    return word_to_number(command)

'''

@Function Name : select_voice
@Description   : Lets the user select a language and voice, plays a sample
                 voice, asks for confirmation, and saves the selected voice.
@InputParam    : None
@OutputParam   : Selected voice

'''

def select_voice():

    from voice import speak
    from voice_recognition import speech

    languages = list(VOICE_OPTIONS.keys())

    # ------------------ Language Selection ------------------

    asyncio.run(speak("Please select a language."))

    print("\n========== Select Language ==========\n")

    for index, language in enumerate(languages, start=1):
        print(f"{index}. {language}")
        asyncio.run(speak(f"{index}. {language}"))

    while True:

        asyncio.run(speak("Please say the language number."))

        command = speech()
        print("Recognized:", repr(command))

        language_choice = get_language_choice(command, languages)

        if language_choice is None:
            asyncio.run(speak("Invalid language selection. Please try again."))
            continue

        if language_choice < 1 or language_choice > len(languages):
            asyncio.run(speak("Invalid language selection."))
            continue

        break

    selected_language = languages[language_choice - 1]

    speech_code = VOICE_OPTIONS[selected_language]["speech"]

    voices = VOICE_OPTIONS[selected_language]["voices"]

# ------------------ Voice Selection ------------------

    asyncio.run(speak(f"You selected {selected_language}."))

    print(f"\n========== {selected_language} Voices ==========\n")

    for index, voice in enumerate(voices, start=1):
       print(f"{index}. {voice}")
       asyncio.run(speak(f"Voice {index}"))

    while True:

       asyncio.run(speak("Please say the voice number."))

    # Always recognize menu selections in English
       command = speech(language="en-IN")

       print("Voice Recognized:", repr(command))

       voice_choice = word_to_number(command)

       if voice_choice is None:
        asyncio.run(speak("Invalid voice selection. Please try again."))
        continue

       if not (1 <= voice_choice <= len(voices)):
        asyncio.run(speak("Invalid voice selection."))
        continue

       selected_voice = voices[voice_choice - 1]

       print("\nSelected Voice:", selected_voice)

    # Play sample
       asyncio.run(
           speak(
                SAMPLE_TEXT[selected_language],
                selected_voice
    )
)

       asyncio.run(speak("Do you want to save this voice? Say yes or no."))

       time.sleep(0.7) 

       answer = speech(language="en-IN")

       print("Raw Answer:", answer)
       print("Answer:", repr(answer))

       if not answer:
        asyncio.run(speak("I didn't hear you."))
        continue

       answer = answer.lower().strip()
       print("Answer:", repr(answer))

       if any(word in answer for word in YES_WORDS):

        save_voice(
            selected_language,
            speech_code,
            selected_voice
        )

        asyncio.run(speak("Voice saved successfully."))

        print("\n========== Voice Saved ==========")
        print("Language :", selected_language)
        print("Speech   :", speech_code)
        print("Voice    :", selected_voice)

        return selected_voice

       elif answer in ["no", "change"]:

        asyncio.run(speak("Please choose another voice."))

       else:

        asyncio.run(speak("Please answer yes or no."))
