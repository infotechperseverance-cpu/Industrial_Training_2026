import webbrowser
import socket
from voice import speak
import config
import asyncio

'''

@Module Name : check_internet
@Description : This module check internet is provide 
@InputParam  : NONE
@OutputParam : True or False
@Author      : Unnati Thakur

'''


def check_internet():
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except:
        return False
    

'''

@Module Name : open_website
@Description : This module open a website
@InputParam  : command(user command want to open)
@OutputParam : NONE
@Author      : Unnati Thakur

'''



def open_website(command):

    if command == "":
        asyncio.run(print("Website name cannot be empty."))
        return

    website = command.lower().strip()

    if website.startswith("open"):
        website = website.replace("open", "").strip()

    if " " in website:
        website = website.replace(" ", "")

    if website.startswith("www."):
        url = "https://" + website

    elif website.startswith("http://") or website.startswith("https://"):
        url = website

    elif "." in website:
        url = "https://" + website

    else:
        url = "https://www." + website + ".com"

    if not check_internet():
        asyncio.run(print("No Internet Connection."))
        return

    try:
        webbrowser.open(url)
        asyncio.run(speak("Website Opened Successfully"))

    except:
        print("Website not found.")

