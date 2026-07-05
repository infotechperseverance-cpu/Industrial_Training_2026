import tkinter as tk
from tkinter import filedialog

def select_folder():
    tk.Tk().withdraw()
    f=filedialog.askdirectory()

    if f=="":
        print("no folder selected")
        return None
    
    print("folder selected")
    return f
f =select_folder()

