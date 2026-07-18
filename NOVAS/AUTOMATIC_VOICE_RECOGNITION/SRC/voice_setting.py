
'''

@Module Name   : Voice_setting.py
@Description   : Lets the user select a language and voice, plays a sample
                 voice, asks for confirmation, and saves the selected voice.
@InputParam    : None
@OutputParam   : Selected voice

'''

import json
import os
from config import DEFAULT_SPEECH_LANGUAGE, DEFAULT_VOICE

FILE_NAME = "voice_data.json"

'''

@Function Name : get_settings
@Description   : Loads the saved voice settings from the JSON file. If the
                 file does not exist, it creates the file with default voice
                 settings. If the file is empty or contains invalid data,
                 default settings are returned.
@InputParam    : None
@OutputParam   : default setting language, speech, and voice settings
@Author        : Vaishnavi Teli

'''

def get_settings():

    default_settings = {
        "language": "English",
        "speech": DEFAULT_SPEECH_LANGUAGE,
        "voice": DEFAULT_VOICE
    }

    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(default_settings, file, indent=4)
        return default_settings

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:

            if os.path.getsize(FILE_NAME) == 0:
                return default_settings

            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return default_settings
    

'''

@Function Name : save_voice
@Description   : Saves the user's selected language, speech recognition
                 language, and voice into the JSON settings file.
@InputParam    : language (String),
                 speech (String),
                 voice (String)
@OutputParam   : None
@Author        : Vaishnavi Teli

'''

def save_voice(language, speech, voice):

    settings = {
        "language": language,
        "speech": speech,
        "voice": voice
    }

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)