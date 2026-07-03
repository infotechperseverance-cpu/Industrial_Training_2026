
import win32com.client

#----This class provides voice responses such as greeting the user,
#----speaking success and error messages, and saying goodbye.
class VoiceResponse:

    #----Converts text into speech using Windows SAPI
    @staticmethod
    def speak(text):
        print(f"Assistant: {text}")
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)

    #----Greets the user when the application starts
    @staticmethod
    def greet():
        VoiceResponse.speak(
            "Hello! I am your Smart Voice Assistant. Ready to help you."
        )

    #----Speaks a confirmation message after a successful command
    @staticmethod
    def success(message):
        VoiceResponse.speak(message)

    #----Speaks an error message when a command fails
    @staticmethod
    def failure(message):
        VoiceResponse.speak(message)
            

    #----Speaks a goodbye message before the application closes
    @staticmethod
    def goodbye():
        VoiceResponse.speak(
            "Thank you for using Smart Voice Assistant. Goodbye!"
        )


# ------------------ Testing ------------------

VoiceResponse.greet()

VoiceResponse.success("Google has been opened successfully.")
VoiceResponse.success("Calculator has been opened successfully.")
VoiceResponse.success("Screenshot captured successfully.")

VoiceResponse.failure("sorry ,i have internet problem")

VoiceResponse.goodbye()