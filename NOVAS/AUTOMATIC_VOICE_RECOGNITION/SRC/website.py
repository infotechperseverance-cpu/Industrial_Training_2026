"""
@Module Name : website.py

@Description : This module dynamically searches for and
               opens websites in the default web browser.

@InputParam  : Website name

@OutputParam : Opens the requested website

@Author      : Vaishnavi Teli
"""

import asyncio
import webbrowser

import requests

from voice import speak


'''
@Function Name : check_url

@Description   : Checks whether the given website URL is
                 accessible.

@InputParam    : url

@OutputParam   : True if the URL exists, otherwise False

@Author        : Vaishnavi Teli
'''
def check_url(url):

    try:

        response = requests.get(
            url,
            timeout=5,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        return response.status_code < 400

    except requests.RequestException:

        return False


'''
@Function Name : find_website

@Description   : Searches for a valid website URL using
                 common domain extensions.

@InputParam    : name

@OutputParam   : Website URL / None

@Author        : bhoomi sapke
'''
def find_website(name):

    name = name.replace(" ", "")

    extensions = [
        ".com",
        ".in",
        ".ac.in",
        ".org",
        ".edu",
        ".gov.in",
        ".net"
    ]

    prefixes = [
        "https://",
        "https://www."
    ]

    for prefix in prefixes:

        for ext in extensions:

            url = prefix + name + ext

            # print("Checking:", url)

            if check_url(url):
                return url

    return None


'''
@Function Name : open_website

@Description   : Finds and opens the requested website in
                 the default web browser.

@InputParam    : command

@OutputParam   : Opens website

@Author        : Vaishnavi Teli
'''
def open_website(command):

    if not command:
        return

    website = command.lower().strip()
    if not website:
        asyncio.run(speak("Please tell me the website name."))
        return
    if website.startswith("open "):
        website = website[5:].strip()

    if website.endswith("website"):
        website = website.replace(
            "website",
            ""
        ).strip()

    print("Finding:", website)

    try:

        url = find_website(website)

        if url:

            print("Opening:", url)

            webbrowser.open(url)

            asyncio.run(
                speak(f"Opening {website}")
            )

        else:

            asyncio.run(
                speak("Website not found.")
            )

    except Exception as e:

        print(f"Website Error: {e}")

        asyncio.run(
            speak("Unable to open the website.")
        )