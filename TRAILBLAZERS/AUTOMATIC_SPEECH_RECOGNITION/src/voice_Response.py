"""
=========================================
Voice Response Module
Purpose:
Handles all voice responses of the Smart Voice Assistant.
=========================================
"""

from voice_engine import speak


class VoiceResponse:

    # Convert text into speech
    @staticmethod
    def speak(text):
        print(f"Assistant: {text}")
        speak(text)

    # Greets the user when the application starts
    @staticmethod
    def greet():
        VoiceResponse.speak(
            "Hello! I am your Smart Voice Assistant. Ready to help you."
        )

    # Speak a success message
    @staticmethod
    def success(message):
        VoiceResponse.speak(message)

    # Speak an error message
    @staticmethod
    def failure(message):
        VoiceResponse.speak(message)

    # Say goodbye to the user
    @staticmethod
    def goodbye():
        VoiceResponse.speak(
            "Thank you for using Smart Voice Assistant. Goodbye!"
        )