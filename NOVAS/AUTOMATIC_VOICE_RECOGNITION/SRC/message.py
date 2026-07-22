from config import MESSAGES
from voice_setting import get_settings

'''

@Function Name : get_message
@Description   : Returns the message in the user's selected language.
@InputParam    : key (Message key)
@OutputParam   : Message (String)
@Author        : Vaishnavi Teli

'''

def get_message(key):

    language = get_settings()["language"]

    return MESSAGES[language].get(key, key)