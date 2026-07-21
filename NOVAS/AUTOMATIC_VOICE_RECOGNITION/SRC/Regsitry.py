
'''

@Module Name         : Registry 
@Description         : This module Launch Windows applications
#                      and websites dynamically
@Inputparam          : None
@OutputPara          : None
@Author              : Vaishnavi Teli

'''


import winreg
import subprocess
import asyncio

from website import open_website
from voice import speak
from message import get_message


class RegistryLauncher:


    def __init__(self):

        self.registry_paths = [

            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"
            ),

            (
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"
            )
        ]


        self.applications = {

            # Browsers
            "chrome": "chrome.exe",
            "edge": "msedge.exe",

            # Windows Apps
            "notepad": "notepad.exe",
            "paint": "mspaint.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "explorer": "explorer.exe",

            # Microsoft Office
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "powerpoint": "POWERPNT.EXE",

            # IDEs
            "vs code": "Code.exe",
            "visual studio code": "Code.exe",

            # Communication
            "whatsapp": "WhatsApp.exe",
            "chatgpt": "ChatGPT.exe",
            "telegram": "Telegram.exe",
            "discord": "Discord.exe",
            "zoom": "Zoom.exe",

            # Design
            "canva": "Canva.exe",
            "figma": "Figma.exe",

            # Development
            "pycharm": "pycharm64.exe",
            "intellij": "idea64.exe",
            "eclipse": "eclipse.exe",

            # Media
            "vlc": "vlc.exe",
            "spotify": "Spotify.exe",

            # Utilities
            "snipping tool": "SnippingTool.exe",
            "task manager": "Taskmgr.exe",
            "control panel": "control.exe",

            # Adobe
            "photoshop": "Photoshop.exe",
            "illustrator": "Illustrator.exe",
            "acrobat": "Acrobat.exe"
        }


    def get_application_path(self, exe_name):

        for hive, registry in self.registry_paths:

            try:

                key = winreg.OpenKey(
                    hive,
                    registry + "\\" + exe_name
                )


                path, _ = winreg.QueryValueEx(
                    key,
                    ""
                )

                winreg.CloseKey(key)

                return path


            except FileNotFoundError:

                continue


        return None



    def launch(self, command):

        command = command.lower().strip()


        if command.startswith("open"):

            app = command.replace(
                "open",
                "",
                1
            ).strip()



            # ==========================
            # Application Opening
            # ==========================

            if app in self.applications:


                exe = self.applications[app]


                # Registry Search

                path = self.get_application_path(exe)


                if path:

                    self.start_app(path, app)

                    return True



                # Windows command fallback

                try:

                    self.start_app(exe, app)

                    return True


                except Exception:
                    pass



            # ==========================
            # Website Opening
            # ==========================


            else:

                open_website(app)

                return True



        asyncio.run(
            speak(get_message("command_not_recognized"))
        )

        return False



    def start_app(self, path, app):

        try:

            subprocess.Popen(path)


            message = get_message(
                "opening"
            ).format(app)


            print(message)


            asyncio.run(
                speak(message)
            )


        except Exception as e:

            print(f"Application Launch Error: {e}")

            asyncio.run(
                speak(
                    "Unable to open application."
                )
            )

'''
@Function Name : process
@Description   : Processes application and website opening commands.
@Input Param   : command
@Output Param  : TRUE if handled, otherwise FALSE.
@Author        : bhoomi sapke
'''

launcher = RegistryLauncher()

def process(command):

    command = command.lower().strip()

    if command.lower().startswith("open"):
        return launcher.launch(command)

    return False