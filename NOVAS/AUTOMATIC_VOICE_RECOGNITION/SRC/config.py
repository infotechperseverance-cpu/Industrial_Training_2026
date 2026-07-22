'''

@Module Name : config.py
@Description : This module stores the common configuration settings used
               throughout the NOVA - Automatic Voice Recognition Assistant.
               It provides centralized constants such as assistant details,
               database configuration, voice settings, and project
               information. All project modules should import the required
               configuration values from this module instead of hardcoding
               them.
@InputParam  : None
@OutputParam : Common configuration constants

'''
import os

# PROJECT INFORMATION

PROJECT_NAME = "NOVA"
PROJECT_VERSION = "1.0"


# ASSISTANT CONFIGURATION

ASSISTANT_NAME = "NOVA"
WELCOME_MESSAGE = f"Hello! I am {ASSISTANT_NAME}. How can I help you?"
WAKE_RESPONSE = "I'm listening."
SLEEP_COMMAND = "Go to sleep"
SLEEP_RESPONSE = "Going to sleep."
WAKE_WORD = f"hi {ASSISTANT_NAME.lower()}"
EXIT_COMMAND = f"exit {ASSISTANT_NAME.lower()}"
TIMEOUT = 10
PHRASE_TIME_LIMIT = 5
DEFAULT_SPEECH_LANGUAGE = "en-IN"

# DATABASE CONFIGURATION

DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "assistant"
DB_USER = "root"
DB_PASSWORD = "BSS2008"

# Exit NOVA

EXIT_COMMANDS = [
    "exit",
    "exit nova",
    "close nova",
    "stop nova",
    "shutdown nova",
    "goodbye"
]


# VOICE CONFIGURATION

DEFAULT_LANGUAGE = "en-IN"
DEFAULT_VOICE = "en-IN-NeerjaNeural"

VOICE_OPTIONS = {

    "English": {
        "speech": "en-IN",
        "voices": [
            "en-IN-NeerjaNeural",
            "en-IN-PrabhatNeural"
        ]
    },

    "Hindi": {
        "speech": "hi-IN",
        "voices": [
            "hi-IN-SwaraNeural",
            "hi-IN-MadhurNeural"
        ]
    },

    "Marathi": {
        "speech": "mr-IN",
        "voices": [
            "mr-IN-AarohiNeural",
            "mr-IN-ManoharNeural"
        ]
    }
}


# ---------------- Number Words ----------------

NUMBER_WORDS = {
    1: ["1", "one", "won", "first", "number one","None","number 1"],
    2: ["2", "two", "to", "too", "second", "number two","number 2"],
    3: ["3", "three", "third", "number three"],
    4: ["4", "four", "for", "fourth", "number four"],
    5: ["5", "five", "fifth", "number five"],
    6: ["6", "six", "sixth", "number six"],
    7: ["7", "seven", "seventh", "number seven"],
    8: ["8", "eight", "ate", "eighth", "number eight"],
    9: ["9", "nine", "ninth", "number nine"],
    10: ["10", "ten", "then", "tenth", "number ten"]
}


# ---------------- Language Aliases ----------------

LANGUAGE_ALIASES = {
    "english": "English",
    "eng": "English",

    "hindi": "Hindi",
    "हिंदी": "Hindi",

    "marathi": "Marathi",
    "मराठी": "Marathi",

}


# ---------------- Default Speech Language ----------------

DEFAULT_SPEECH_LANGUAGE = "en-IN"

#------------------ Sample Text -----------------------

SAMPLE_TEXT = {
    "English": "Hello. This is a sample voice.",
    "Hindi": "नमस्ते। यह चुनी गई आवाज़ का नमूना है।",
    "Marathi": "नमस्कार. हा निवडलेल्या आवाजाचा नमुना आहे.",
}

YES_WORDS = [
    "yes",
    "yeah",
    "ok",
    "okay",
    "save",
    "confirm",
    "enable",
    "yes ok",
    "select"
]

NO_WORDS = [
    "no",
    "change",
    "cancel",
    "disable"
]


SETTINGS_TEXT = {
    "en-IN": {
        "opening": "Opening settings.",
        "menu": """Settings
        1. Change Language and Voice
        2. Brightness Control
        3. Shutdown Laptop
        4. Exit""",
        "prompt": "Say change language and voice, brightness, shutdown laptop or exit."
    },

    "hi-IN": {
        "opening": "सेटिंग्स खोल रहा हूँ।",
        "menu": """सेटिंग्स
        1. भाषा और आवाज़ बदलें
        2. ब्राइटनेस कंट्रोल
        3. लैपटॉप बंद करें
        4. बाहर निकलें""",
        "prompt": "भाषा और आवाज़ बदलें, ब्राइटनेस, लैपटॉप बंद करें या बाहर निकलें।"
    },

    "mr-IN": {
        "opening": "सेटिंग्ज उघडत आहे.",
        "menu": """सेटिंग्ज
        1. भाषा आणि आवाज बदला
        2. ब्राइटनेस कंट्रोल
        3. लॅपटॉप बंद करा
        4. बाहेर पडा""",
        "prompt": "भाषा आणि आवाज बदला, ब्राइटनेस, लॅपटॉप बंद करा किंवा बाहेर पडा."
    }
}

# SYSTEM CONFIGURATION

USERNAME = os.getlogin()

HOME_DIRECTORY = os.path.expanduser("~")

DEFAULT_SEARCH_PATHS = [
    os.path.join(HOME_DIRECTORY, "Desktop"),
    os.path.join(HOME_DIRECTORY, "Documents"),
    os.path.join(HOME_DIRECTORY, "Downloads"),
    HOME_DIRECTORY
]

MESSAGES =  {

    "English": {

        "opening": "Opening {}...",
        "unknown_application": "Unknown application.",
        "application_not_found": "Application not found.",
        "opening_google": "Opening Google Search.",
        "listening": "I'm listening.",
        "sleep": "Going to sleep.",
        "closing": "Closing NOVA.",
        "no_speech": "No speech detected.",
        "speech_error": "Speech recognition service unavailable.",
        "voice_saved": "Voice saved successfully.",
        "please_select_language": "Please select a language.",
        "select_language": "Select Language.",
        "say_language_number": "Please say the language number.",
        "invalid_language_selection": "Invalid language selection. Please try again.",
        "you_selected": "You selected.",
        "voices": "Voices.",
        "say_voice_number": "Please say the voice number.",
        "invalid_voice_selection": "Invalid voice selection. Please try again.",
        "selected_voice": "Selected Voice.",
        "save_voice_question": "Do you want to save this voice? Say yes or no.",
        "didnt_hear": "I didn't hear you.",
        "choose_another_voice": "Please choose another voice.",
        "answer_yes_no": "Please answer yes or no.",
        "website_empty": "Website name cannot be empty.",
        "no_internet": "No Internet Connection.",
        "website_opened": "Website Opened Successfully.",
        "website_not_found": "Website not found.",
        "google_api_error": "Google Speech API Error.",
        "opening_settings": "Opening settings.",
        "settings_command": "Say change language and voice, brightness, shutdown laptop or back.",
        "brightness_command": "Say increase brightness, decrease brightness or set brightness.",
        "brightness_increased": "Brightness increased.",
        "brightness_decreased": "Brightness decreased.",
        "brightness_set": "Brightness set to {value} percent.",
        "brightness_not_detected": "Brightness value not detected.",
        "invalid_brightness": "Invalid brightness command.",
        "brightness_not_supported": "Brightness control is not supported on this device.",
        "shutdown_message": "Shutting down your laptop in ten seconds.",
        "command_not_recognized": "Command not recognized.",
        "application_launch_error": "Application Launch Error.",
        "unable_open_application": "Unable to open application.",
        "settings": "SETTINGS",
        "change_language_voice": "1. Change Language and Voice",
        "brightness_control": "2. Brightness Control",
        "shutdown_laptop_option": "3. Shutdown Laptop",
        "exit_option": "4. Exit",

        "invalid_file_folder_command" : "Invalid file or folder command.",
        "ask_folder_name": "What should be the folder name?",
        "no_folder_name_received": "No folder name received.",
        "ask_folder_location": "Where do you want to create this folder?",
        "no_parent_folder_received": "No parent folder received.",
        "searching_destination_folder": "Searching for the destination folder...",
        "destination_folder_found": "Destination folder found.",
        "folder_created_successfully": "Folder created successfully.",
        "unable_to_create_folder": "Unable to create folder.",
        "parent_folder_not_found": "Parent folder not found.",

        "ask_file_name_with_extension": "What should be the file name with extension?",
        "no_file_name_received": "No file name received.",
        "ask_file_location": "Where do you want to create this file?",
        "file_created_successfully": "File created successfully.",
        "unable_to_create_file": "Unable to create file.",

        "ask_file_name": "What is the file name?",
        "searching_file": "Searching for the file...",
        "file_found_deleting": "File found. Deleting file.",
        "file_deleted_successfully": "File deleted successfully.",
        "unable_to_delete_file": "Unable to delete file.",
        "file_not_found": "File not found.",

        "ask_folder_name_delete": "What is the folder name?",
        "searching_folder": "Searching for the folder...",
        "deleting": "Deleting:",
        "folder_found_deleting": "Folder found. Deleting folder.",
        "unable_to_delete_folder": "Unable to delete folder.",
        "folder_deleted_successfully": "Folder deleted successfully.",
        "folder_not_found": "Folder not found.",

        "file_found": "File found.",
        "opening_file": "Opening file.",
        "unable_to_open_file": "Unable to open file.",

        "opening_folder": "Opening folder.",
        "unable_to_open_folder": "Unable to open folder.",

        "folder_already_exists": "Folder already exists."


    },

    "Hindi": {
        "opening": "{} खोल रहा हूँ...",
        "unknown_application": "एप्लिकेशन पहचान में नहीं आया।",
        "application_not_found": "एप्लिकेशन नहीं मिला।",
        "opening_google": "गूगल सर्च खोल रहा हूँ।",
        "listening": "मैं सुन रहा हूँ।",
        "sleep": "स्लीप मोड में जा रहा हूँ।",
        "closing": "नोवा बंद कर रहा हूँ।",
        "no_speech": "कोई आवाज़ नहीं मिली।",
        "speech_error": "स्पीच सेवा उपलब्ध नहीं है।",
        "voice_saved": "आवाज़ सफलतापूर्वक सहेज ली गई।",
        "please_select_language": "कृपया एक भाषा चुनें।",
        "select_language": "भाषा चुनें।",
        "say_language_number": "कृपया भाषा का नंबर बोलें।",
        "invalid_language_selection_retry": "अमान्य भाषा चयन। कृपया पुनः प्रयास करें।",
        "invalid_language_selection": "अमान्य भाषा चयन।",
        "you_selected": "आपने चुना है।",
        "voices": "आवाज़ें।",
        "say_voice_number": "कृपया आवाज़ का नंबर बोलें।",
        "invalid_voice_selection_retry": "अमान्य आवाज़ चयन। कृपया पुनः प्रयास करें।",
        "invalid_voice_selection": "अमान्य आवाज़ चयन।",
        "selected_voice": "चयनित आवाज़:",
        "save_voice_confirmation": "क्या आप इस आवाज़ को सहेजना चाहते हैं? हाँ या नहीं कहें।",
        "didnt_hear_you": "मैं आपकी आवाज़ नहीं सुन पाया।",
        "voice_saved": "आवाज़ सफलतापूर्वक सहेजी गई।",
        "choose_another_voice": "कृपया दूसरी आवाज़ चुनें।",
        "answer_yes_no": "कृपया हाँ या नहीं में उत्तर दें।",
        "website_name_empty": "वेबसाइट का नाम खाली नहीं हो सकता।",
        "no_internet": "इंटरनेट कनेक्शन नहीं है।",
        "website_opened": "वेबसाइट सफलतापूर्वक खोली गई।",
        "website_not_found": "वेबसाइट नहीं मिली।",
        "google_speech_api_error": "गूगल स्पीच API त्रुटि:",
        "opening_settings": "सेटिंग्स खोली जा रही हैं।",
        "settings_options": "भाषा और आवाज़ बदलें, ब्राइटनेस, लैपटॉप बंद करें या वापस कहें।",
        "brightness_options": "ब्राइटनेस बढ़ाएँ, घटाएँ या सेट करें कहें।",
        "brightness_increased": "ब्राइटनेस बढ़ा दी गई है।",
        "brightness_decreased": "ब्राइटनेस घटा दी गई है।",
        "brightness_set": "ब्राइटनेस {value} प्रतिशत पर सेट की गई है।",
        "brightness_value_not_detected": "ब्राइटनेस का मान नहीं मिला।",
        "invalid_brightness_command": "अमान्य ब्राइटनेस कमांड।",
        "brightness_not_supported": "यह डिवाइस ब्राइटनेस नियंत्रण का समर्थन नहीं करता।",
        "shutdown_laptop": "आपका लैपटॉप दस सेकंड में बंद होगा।",
        "settings_command_prompt": "कृपया भाषा और आवाज़ बदलें, ब्राइटनेस, लैपटॉप बंद करें या वापस कहें।",
        "command_not_recognized": "कमांड पहचानी नहीं गई।",
        "application_launch_error": "एप्लिकेशन लॉन्च त्रुटि:",
        "unable_to_open_application": "एप्लिकेशन खोलने में असमर्थ।",
        "settings": "सेटिंग्स",
        "change_language_voice": "1. भाषा और आवाज़ बदलें",
        "brightness_control": "2. ब्राइटनेस नियंत्रण",
        "shutdown_laptop_option": "3. लैपटॉप बंद करें",
        "exit_option": "4. बाहर निकलें",

        "invalid_file_folder_command": "अमान्य फ़ाइल या फ़ोल्डर कमांड।",
        "ask_folder_name": "फ़ोल्डर का नाम क्या होना चाहिए?",
        "no_folder_name_received": "फ़ोल्डर का नाम प्राप्त नहीं हुआ।",
        "ask_folder_location": "आप यह फ़ोल्डर कहाँ बनाना चाहते हैं?",
        "no_parent_folder_received": "पैरेंट फ़ोल्डर प्राप्त नहीं हुआ।",
        "searching_destination_folder": "गंतव्य फ़ोल्डर खोजा जा रहा है...",
        "destination_folder_found": "गंतव्य फ़ोल्डर मिल गया।",
        "folder_created_successfully": "फ़ोल्डर सफलतापूर्वक बनाया गया।",
        "unable_to_create_folder": "फ़ोल्डर बनाने में असमर्थ।",
        "parent_folder_not_found": "पैरेंट फ़ोल्डर नहीं मिला।",

        "ask_file_name_with_extension": "एक्सटेंशन सहित फ़ाइल का नाम क्या होना चाहिए?",
        "no_file_name_received": "फ़ाइल का नाम प्राप्त नहीं हुआ।",
        "ask_file_location": "आप यह फ़ाइल कहाँ बनाना चाहते हैं?",
        "file_created_successfully": "फ़ाइल सफलतापूर्वक बनाई गई।",
        "unable_to_create_file": "फ़ाइल बनाने में असमर्थ।",

        "ask_file_name": "फ़ाइल का नाम क्या है?",
        "searching_file": "फ़ाइल खोजी जा रही है...",
        "file_found_deleting": "फ़ाइल मिल गई। फ़ाइल हटाई जा रही है।",
        "file_deleted_successfully": "फ़ाइल सफलतापूर्वक हटा दी गई।",
        "unable_to_delete_file": "फ़ाइल हटाने में असमर्थ।",
        "file_not_found": "फ़ाइल नहीं मिली।",

        "ask_folder_name_delete": "फ़ोल्डर का नाम क्या है?",
        "searching_folder": "फ़ोल्डर खोजा जा रहा है...",
        "deleting": "हटाया जा रहा है:",
        "folder_found_deleting": "फ़ोल्डर मिल गया। फ़ोल्डर हटाया जा रहा है।",
        "unable_to_delete_folder": "फ़ोल्डर हटाने में असमर्थ।",
        "folder_deleted_successfully": "फ़ोल्डर सफलतापूर्वक हटा दिया गया।",
        "folder_not_found": "फ़ोल्डर नहीं मिला।",

        "file_found": "फ़ाइल मिल गई।",
        "opening_file": "फ़ाइल खोली जा रही है।",
        "unable_to_open_file": "फ़ाइल खोलने में असमर्थ।",

        "opening_folder": "फ़ोल्डर खोला जा रहा है।",
        "unable_to_open_folder": "फ़ोल्डर खोलने में असमर्थ।",

        "folder_already_exists": "फ़ोल्डर पहले से मौजूद है।"


    },

    "Marathi": {
        "opening": "{} उघडत आहे...",
        "unknown_application": "अनुप्रयोग ओळखता आला नाही.",
        "application_not_found": "अनुप्रयोग सापडला नाही.",
        "opening_google": "Google Search उघडत आहे.",
        "listening": "मी ऐकत आहे.",
        "sleep": "स्लीप मोडमध्ये जात आहे.",
        "closing": "नोव्हा बंद करत आहे.",
        "no_speech": "कोणताही आवाज ऐकू आला नाही.",
        "speech_error": "स्पीच सेवा उपलब्ध नाही.",
        "voice_saved": "आवाज यशस्वीरित्या जतन केला.",
        "please_select_language": "कृपया भाषा निवडा.",
        "select_language": "भाषा निवडा.",
        "say_language_number": "कृपया भाषेचा क्रमांक सांगा.",
        "invalid_language_selection_retry": "अवैध भाषा निवड. कृपया पुन्हा प्रयत्न करा.",
        "invalid_language_selection": "अवैध भाषा निवड.",
        "you_selected": "तुम्ही निवडले.",
        "voices": "आवाज.",
        "say_voice_number": "कृपया आवाजाचा क्रमांक सांगा.",
        "invalid_voice_selection_retry": "अवैध आवाज निवड. कृपया पुन्हा प्रयत्न करा.",
        "invalid_voice_selection": "अवैध आवाज निवड.",
        "selected_voice": "निवडलेला आवाज:",
        "save_voice_confirmation": "तुम्हाला हा आवाज जतन करायचा आहे का? होय किंवा नाही म्हणा.",
        "didnt_hear_you": "मी तुमचा आवाज ऐकू शकलो नाही.",
        "voice_saved": "आवाज यशस्वीरित्या जतन केला.",
        "choose_another_voice": "कृपया दुसरा आवाज निवडा.",
        "answer_yes_no": "कृपया होय किंवा नाही असे उत्तर द्या.",
        "website_name_empty": "वेबसाइटचे नाव रिकामे असू शकत नाही.",
        "no_internet": "इंटरनेट कनेक्शन नाही.",
        "website_opened": "वेबसाइट यशस्वीरित्या उघडली.",
        "website_not_found": "वेबसाइट सापडली नाही.",
        "google_speech_api_error": "Google Speech API त्रुटी:",
        "opening_settings": "सेटिंग्ज उघडत आहे.",
        "settings_options": "भाषा आणि आवाज बदला, ब्राइटनेस, लॅपटॉप बंद करा किंवा मागे म्हणा.",
        "brightness_options": "ब्राइटनेस वाढवा, कमी करा किंवा सेट करा म्हणा.",
        "brightness_increased": "ब्राइटनेस वाढवला आहे.",
        "brightness_decreased": "ब्राइटनेस कमी केला आहे.",
        "brightness_set": "ब्राइटनेस {value} टक्के सेट केला आहे.",
        "brightness_value_not_detected": "ब्राइटनेस मूल्य आढळले नाही.",
        "invalid_brightness_command": "अवैध ब्राइटनेस कमांड.",
        "brightness_not_supported": "या डिव्हाइसवर ब्राइटनेस नियंत्रण समर्थित नाही.",
        "shutdown_laptop": "तुमचा लॅपटॉप दहा सेकंदात बंद होईल.",
        "settings_command_prompt": "कृपया भाषा आणि आवाज बदला, ब्राइटनेस, लॅपटॉप बंद करा किंवा मागे म्हणा.",
        "command_not_recognized": "कमांड ओळखली गेली नाही.",
        "application_launch_error": "अॅप्लिकेशन सुरू करताना त्रुटी:",
        "unable_to_open_application": "अॅप्लिकेशन उघडता आले नाही.",
        "change_language_voice": "1. भाषा आणि आवाज बदला",
        "brightness_control": "2. ब्राइटनेस नियंत्रण",
        "shutdown_laptop_option": "3. लॅपटॉप बंद करा",
        "exit_option": "4. बाहेर पडा",


        "invalid_file_folder_command": "अवैध फाइल किंवा फोल्डर कमांड.",
        "ask_folder_name": "फोल्डरचे नाव काय असावे?",
        "no_folder_name_received": "फोल्डरचे नाव प्राप्त झाले नाही.",
        "ask_folder_location": "हा फोल्डर कुठे तयार करायचा आहे?",
        "no_parent_folder_received": "पॅरेंट फोल्डर प्राप्त झाला नाही.",
        "searching_destination_folder": "गंतव्य फोल्डर शोधत आहे...",
        "destination_folder_found": "गंतव्य फोल्डर सापडला.",
        "folder_created_successfully": "फोल्डर यशस्वीरित्या तयार केला.",
        "unable_to_create_folder": "फोल्डर तयार करता आला नाही.",
        "parent_folder_not_found": "पॅरेंट फोल्डर सापडला नाही.",

        "ask_file_name_with_extension": "एक्स्टेन्शनसह फाइलचे नाव काय असावे?",
        "no_file_name_received": "फाइलचे नाव प्राप्त झाले नाही.",
        "ask_file_location": "ही फाइल कुठे तयार करायची आहे?",
        "file_created_successfully": "फाइल यशस्वीरित्या तयार केली.",
        "unable_to_create_file": "फाइल तयार करता आली नाही.",

        "ask_file_name": "फाइलचे नाव काय आहे?",
        "searching_file": "फाइल शोधत आहे...",
        "file_found_deleting": "फाइल सापडली. फाइल हटवत आहे.",
        "file_deleted_successfully": "फाइल यशस्वीरित्या हटवली.",
        "unable_to_delete_file": "फाइल हटवता आली नाही.",
        "file_not_found": "फाइल सापडली नाही.",

        "ask_folder_name_delete": "फोल्डरचे नाव काय आहे?",
        "searching_folder": "फोल्डर शोधत आहे...",
        "deleting": "हटवत आहे:",
        "folder_found_deleting": "फोल्डर सापडला. फोल्डर हटवत आहे.",
        "unable_to_delete_folder": "फोल्डर हटवता आला नाही.",
        "folder_deleted_successfully": "फोल्डर यशस्वीरित्या हटवला.",
        "folder_not_found": "फोल्डर सापडला नाही.",

        "file_found": "फाइल सापडली.",
        "opening_file": "फाइल उघडत आहे.",
        "unable_to_open_file": "फाइल उघडता आली नाही.",

        "opening_folder": "फोल्डर उघडत आहे.",
        "unable_to_open_folder": "फोल्डर उघडता आला नाही.",

        "folder_already_exists": "फोल्डर आधीपासून अस्तित्वात आहे."
    }
}