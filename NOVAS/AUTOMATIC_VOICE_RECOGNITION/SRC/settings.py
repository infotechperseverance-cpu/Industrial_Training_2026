import asyncio
import os
import screen_brightness_control as sbc

from voice import speak
from voice_customization import select_voice


def open_settings():
  while True:

    asyncio.run(
        speak("Opening settings.")
    )

    print("""
========== SETTINGS ==========
1. Change Language and Voice
2. Brightness Control
3. Shutdown Laptop
4. Back
""")

    asyncio.run(
        speak(
            "Say change language and voice, brightness, shutdown laptop or back."
        )
    )

    from voice_recognition import speech

    command = speech()

    if not command:
        return

    command = command.lower()

    # ---------- Language & Voice ----------

    if "language" in command or "voice" in command:

        select_voice()
        continue

    # ---------- Brightness ----------

    elif "brightness" in command:

        asyncio.run(
            speak("Say increase brightness, decrease brightness or set brightness.")
        )

        cmd = speech()

        if not cmd:
            return

        cmd = cmd.lower()

        try:

            current = sbc.get_brightness(display=0)[0]

            if "increase" in cmd:

                sbc.set_brightness(min(current + 10, 100))

                asyncio.run(
                    speak("Brightness increased.")
                )

            elif "decrease" in cmd:

                sbc.set_brightness(max(current - 10, 0))

                asyncio.run(
                    speak("Brightness decreased.")
                )

            elif "set" in cmd:

                number = "".join(filter(str.isdigit, cmd))

                if number != "":

                    value = int(number)

                    if value > 100:
                        value = 100

                    if value < 0:
                        value = 0

                    sbc.set_brightness(value)

                    asyncio.run(
                        speak(f"Brightness set to {value} percent.")
                    )

                else:

                    asyncio.run(
                        speak("Brightness value not detected.")
                    )

            else:

                asyncio.run(
                    speak("Invalid brightness command.")
                )

        except Exception:

            asyncio.run(
                speak("Brightness control is not supported on this device.")
            )

        continue

    # ---------- Shutdown ----------

    elif "shutdown" in command:

        asyncio.run(
            speak("Shutting down your laptop in ten seconds.")
        )

        os.system("shutdown /s /t 10")

        return

    # ---------- Back ----------

    elif "back" in command:
        return

    # ---------- Invalid ----------

    else:

        asyncio.run(
            speak("Please say change language and voice, brightness, shutdown laptop or back.")
        )