'''

@Module Name : laptop_setting.py
@Description : This module performs operations on 
               brightness control and shut down 
               the laptop 
@InputParam  : cmd (user command )
@OutputParam : None
@Author      : Unnati Thakur 

'''


import asyncio
from voice import speak
from voice_recognition import speech
import screen_brightness_control as sbc
import os


def brightness(cmd):
        
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

    except Exception as e:
        print(f"Brightness Error: {e}")
        asyncio.run(
            speak("Brightness control is not supported on this device.")
        )

def shutdown():
        asyncio.run(
            speak("Shutting down your laptop in ten seconds.")
        )

        os.system("shutdown /s /t 10")

        return
