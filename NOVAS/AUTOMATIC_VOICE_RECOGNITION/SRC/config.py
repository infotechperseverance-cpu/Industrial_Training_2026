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
PHARSE_TIME_LIMIT = 5
DEFAULT_SPEECH_LANGUAGE = "en-IN"

# DATABASE CONFIGURATION

DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "NOVA"
DB_USER = "root"
DB_PASSWORD = "BSS2008"


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
    },

    "Gujarati": {
        "speech": "gu-IN",
        "voices": [
            "gu-IN-DhwaniNeural",
            "gu-IN-NiranjanNeural"
        ]
    },

    "Bengali": {
        "speech": "bn-IN",
        "voices": [
            "bn-IN-TanishaaNeural",
            "bn-IN-BashkarNeural"
        ]
    },

    "Kannada": {
        "speech": "kn-IN",
        "voices": [
            "kn-IN-SapnaNeural",
            "kn-IN-GaganNeural"
        ]
    },

    "Malayalam": {
        "speech": "ml-IN",
        "voices": [
            "ml-IN-SobhanaNeural",
            "ml-IN-MidhunNeural"
        ]
    },

    "Tamil": {
        "speech": "ta-IN",
        "voices": [
            "ta-IN-PallaviNeural",
            "ta-IN-ValluvarNeural"
        ]
    },

    "Telugu": {
        "speech": "te-IN",
        "voices": [
            "te-IN-ShrutiNeural",
            "te-IN-MohanNeural"
        ]
    },

    "Punjabi": {
        "speech": "pa-IN",
        "voices": [
            "pa-IN-GurleenNeural",
            "pa-IN-VaaniNeural"
        ]
    }
}

MESSAGES = {

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
        "voice_saved": "Voice saved successfully."
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
        "voice_saved": "आवाज़ सफलतापूर्वक सहेज ली गई।"
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
        "voice_saved": "आवाज यशस्वीरित्या जतन केला."
    },

    "Gujarati": {
        "opening": "{} ખોલી રહ્યો છું...",
        "unknown_application": "એપ્લિકેશન ઓળખી શકાયું નથી.",
        "application_not_found": "એપ્લિકેશન મળ્યું નથી.",
        "opening_google": "Google Search ખોલી રહ્યો છું.",
        "listening": "હું સાંભળી રહ્યો છું.",
        "sleep": "સ્લીપ મોડમાં જઈ રહ્યો છું.",
        "closing": "નોવા બંધ કરી રહ્યો છું.",
        "no_speech": "કોઈ અવાજ મળ્યો નથી.",
        "speech_error": "સ્પીચ સેવા ઉપલબ્ધ નથી.",
        "voice_saved": "અવાજ સફળતાપૂર્વક સાચવ્યો."
    },

    "Bengali": {
        "opening": "{} খুলছি...",
        "unknown_application": "অ্যাপ্লিকেশন সনাক্ত করা যায়নি।",
        "application_not_found": "অ্যাপ্লিকেশন পাওয়া যায়নি।",
        "opening_google": "Google Search খুলছি।",
        "listening": "আমি শুনছি।",
        "sleep": "স্লিপ মোডে যাচ্ছি।",
        "closing": "নোভা বন্ধ করছি।",
        "no_speech": "কোনও শব্দ শোনা যায়নি।",
        "speech_error": "স্পিচ সার্ভিস উপলব্ধ নয়।",
        "voice_saved": "ভয়েস সফলভাবে সংরক্ষণ করা হয়েছে।"
    },

    "Kannada": {
        "opening": "{} ತೆರೆಯುತ್ತಿದ್ದೇನೆ...",
        "unknown_application": "ಅಪ್ಲಿಕೇಶನ್ ಗುರುತಿಸಲಾಗಲಿಲ್ಲ.",
        "application_not_found": "ಅಪ್ಲಿಕೇಶನ್ ಸಿಗಲಿಲ್ಲ.",
        "opening_google": "Google Search ತೆರೆಯುತ್ತಿದ್ದೇನೆ.",
        "listening": "ನಾನು ಕೇಳುತ್ತಿದ್ದೇನೆ.",
        "sleep": "ಸ್ಲೀಪ್ ಮೋಡ್‌ಗೆ ಹೋಗುತ್ತಿದ್ದೇನೆ.",
        "closing": "ನೋವಾ ಮುಚ್ಚಲಾಗುತ್ತಿದೆ.",
        "no_speech": "ಯಾವ ಧ್ವನಿಯೂ ಕಂಡುಬಂದಿಲ್ಲ.",
        "speech_error": "ಸ್ಪೀಚ್ ಸೇವೆ ಲಭ್ಯವಿಲ್ಲ.",
        "voice_saved": "ಧ್ವನಿ ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ."
    },

    "Malayalam": {
        "opening": "{} തുറക്കുന്നു...",
        "unknown_application": "ആപ്ലിക്കേഷൻ കണ്ടെത്താനായില്ല.",
        "application_not_found": "ആപ്ലിക്കേഷൻ ലഭ്യമായില്ല.",
        "opening_google": "Google Search തുറക്കുന്നു.",
        "listening": "ഞാൻ കേൾക്കുന്നു.",
        "sleep": "സ്ലീപ്പ് മോഡിലേക്ക് പോകുന്നു.",
        "closing": "നോവ അടയ്ക്കുന്നു.",
        "no_speech": "ശബ്ദം കണ്ടെത്തിയില്ല.",
        "speech_error": "സ്പീച്ച് സേവനം ലഭ്യമല്ല.",
        "voice_saved": "ശബ്ദം വിജയകരമായി സേവ് ചെയ്തു."
    },

    "Tamil": {
        "opening": "{} திறக்கிறேன்...",
        "unknown_application": "பயன்பாடு கண்டறியப்படவில்லை.",
        "application_not_found": "பயன்பாடு கிடைக்கவில்லை.",
        "opening_google": "Google Search திறக்கிறேன்.",
        "listening": "நான் கேட்கிறேன்.",
        "sleep": "ஸ்லீப் முறைக்கு செல்கிறேன்.",
        "closing": "நோவாவை மூடுகிறேன்.",
        "no_speech": "எந்த குரலும் கண்டறியப்படவில்லை.",
        "speech_error": "குரல் சேவை கிடைக்கவில்லை.",
        "voice_saved": "குரல் வெற்றிகரமாக சேமிக்கப்பட்டது."
    },

    "Telugu": {
        "opening": "{} తెరుస్తున్నాను...",
        "unknown_application": "అప్లికేషన్ గుర్తించబడలేదు.",
        "application_not_found": "అప్లికేషన్ కనబడలేదు.",
        "opening_google": "Google Search తెరుస్తున్నాను.",
        "listening": "నేను వింటున్నాను.",
        "sleep": "స్లీప్ మోడ్‌లోకి వెళ్తున్నాను.",
        "closing": "నోవాను మూసివేస్తున్నాను.",
        "no_speech": "శబ్దం గుర్తించబడలేదు.",
        "speech_error": "స్పీచ్ సేవ అందుబాటులో లేదు.",
        "voice_saved": "వాయిస్ విజయవంతంగా సేవ్ చేయబడింది."
    },

    "Punjabi": {
        "opening": "{} ਖੋਲ੍ਹ ਰਿਹਾ ਹਾਂ...",
        "unknown_application": "ਐਪਲੀਕੇਸ਼ਨ ਨਹੀਂ ਮਿਲੀ।",
        "application_not_found": "ਐਪਲੀਕੇਸ਼ਨ ਉਪਲਬਧ ਨਹੀਂ ਹੈ।",
        "opening_google": "Google Search ਖੋਲ੍ਹ ਰਿਹਾ ਹਾਂ।",
        "listening": "ਮੈਂ ਸੁਣ ਰਿਹਾ ਹਾਂ।",
        "sleep": "ਸਲੀਪ ਮੋਡ ਵਿੱਚ ਜਾ ਰਿਹਾ ਹਾਂ।",
        "closing": "ਨੋਵਾ ਬੰਦ ਕਰ ਰਿਹਾ ਹਾਂ।",
        "no_speech": "ਕੋਈ ਆਵਾਜ਼ ਨਹੀਂ ਮਿਲੀ।",
        "speech_error": "ਸਪੀਚ ਸੇਵਾ ਉਪਲਬਧ ਨਹੀਂ ਹੈ।",
        "voice_saved": "ਆਵਾਜ਼ ਸਫਲਤਾਪੂਰਵਕ ਸੇਵ ਹੋ ਗਈ।"
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

    "gujarati": "Gujarati",
    "ગુજરાતી": "Gujarati",

    "bengali": "Bengali",
    "bangla": "Bengali",
    "বাংলা": "Bengali",

    "kannada": "Kannada",
    "ಕನ್ನಡ": "Kannada",

    "malayalam": "Malayalam",
    "മലയാളം": "Malayalam",

    "tamil": "Tamil",
    "தமிழ்": "Tamil",

    "telugu": "Telugu",
    "తెలుగు": "Telugu",

    "punjabi": "Punjabi",
    "ਪੰਜਾਬੀ": "Punjabi"
}


# ---------------- Default Speech Language ----------------

DEFAULT_SPEECH_LANGUAGE = "en-IN"

#------------------ Sample Text -----------------------

SAMPLE_TEXT = {
    "English": "Hello. This is a sample voice.",
    "Hindi": "नमस्ते। यह चुनी गई आवाज़ का नमूना है।",
    "Marathi": "नमस्कार. हा निवडलेल्या आवाजाचा नमुना आहे.",
    "Gujarati": "નમસ્તે. આ પસંદ કરેલા અવાજનો નમૂનો છે.",
    "Bengali": "নমস্কার। এটি নির্বাচিত কণ্ঠের একটি নমুনা।",
    "Kannada": "ನಮಸ್ಕಾರ. ಇದು ಆಯ್ಕೆ ಮಾಡಿದ ಧ್ವನಿಯ ಮಾದರಿ.",
    "Malayalam": "നമസ്കാരം. ഇത് തിരഞ്ഞെടുത്ത ശബ്ദത്തിന്റെ മാതൃകയാണ്.",
    "Tamil": "வணக்கம். இது தேர்ந்தெடுக்கப்பட்ட குரலின் மாதிரி.",
    "Telugu": "నమస్కారం. ఇది ఎంచుకున్న స్వరానికి నమూనా.",
    "Punjabi": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ। ਇਹ ਚੁਣੀ ਹੋਈ ਆਵਾਜ਼ ਦਾ ਨਮੂਨਾ ਹੈ."
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

import os

# SYSTEM CONFIGURATION

USERNAME = os.getlogin()

HOME_DIRECTORY = os.path.expanduser("~")

DEFAULT_SEARCH_PATHS = [
    os.path.join(HOME_DIRECTORY, "Desktop"),
    os.path.join(HOME_DIRECTORY, "Documents"),
    os.path.join(HOME_DIRECTORY, "Downloads"),
    HOME_DIRECTORY
]