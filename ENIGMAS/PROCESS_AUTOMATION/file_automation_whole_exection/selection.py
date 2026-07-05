import tkinter as tk
from tkinter import filedialog

def select_folder():
    try:

        tk.Tk().withdraw()
        f=filedialog.askdirectory()

        if f=="":
            print("no folder selected")
            return None
        
        print("folder selected")
        return f
    except :
        print("something want wrong")
        return None


