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

@Author      : Bhoomi Sapke

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
PHARSE_TIME_LIMIT = 20


# DATABASE CONFIGURATION

DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "NOVA"
DB_USER = "root"
DB_PASSWORD = "BSS2008"


# VOICE CONFIGURATION

DEFAULT_LANGUAGE = "en-IN"
DEFAULT_VOICE = "Female"
