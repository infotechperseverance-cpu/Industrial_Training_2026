import winreg
import subprocess
from website import open_website
from voice import speak


'''

@Module Name (Class)      : RegistryLauncher
@Description              : This constructor initializes the registry paths in 
                            constructor and stores the application names with 
                            their executable file names.
@InputParam               : NONE
@OutputParam              : Registry paths and application list are initialized.
@Author                   : Vaishnavi Teli

'''


class RegistryLauncher:

    def __init__(self):

        self.registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE,
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),

            (winreg.HKEY_CURRENT_USER,
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths")
        ]

        # Voice command -> executable
        self.applications = {
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "notepad": "notepad.exe",
            "paint": "mspaint.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "explorer": "explorer.exe",
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "powerpoint": "POWERPNT.EXE",
            "vs code": "Code.exe"
        }

    '''

       @Module Name (Method)  : get_application_path
       @Description           : This method searches the Windows Registry for the
                                specified application and returns its executable path.
       @InputParam            : exe_name (Name of the executable file.)
       @OutputParam           : Returns the application path if found; otherwise,
                                returns NONE.
       @Author                : Vaishnavi Teli

    '''

    def get_application_path(self, exe_name):

        for hive, registry in self.registry_paths:

            try:
                key = winreg.OpenKey(
                    hive,
                    registry + "\\" + exe_name
                )

                path, _ = winreg.QueryValueEx(key, "")

                winreg.CloseKey(key)

                return path

            except FileNotFoundError:
                continue

        return None
    
    
    '''

        @Module Name (Method)     : launch
        @Description              : This method open a app its find otherwise,
                                    its search on browser and then open like 
                                    website
        @InputParam               : command (user command)
        @OutputParam              : NONE
        @Author                   : Vaishnavi Teli

    '''



    def launch(self, command):


        command = command.lower()

        if command.startswith("open "):
            app = command.replace("open ", "").strip()
         
            exe = self.applications.get(app)
    
            if exe:

                path = self.get_application_path(exe)
              
                if path:

                    speak(f"Opening {app}...")
                    print(f"Opening {app}...")

                else:

                    print("Application not found.")
                    speak("Opening Google Search...")

                    open_website(app)
            else:

                print("Unknown application.")
                
                open_website(app)