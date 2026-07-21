"""
@Module Name : search_module.py

@Description : This module performs dynamic web searches.
               It extracts the search query from the user's
               command, opens Google Search in the default
               web browser, and provides voice feedback.

@InputParam  : User command

@OutputParam : Opens Google Search in the browser

@Author      : Bhoomi Sapke
"""

import webbrowser
import urllib.parse
import asyncio

from voice import speak


'''
@Function Name : web_search

@Description   : Performs a Google search based on the
                 user's voice command.

@InputParam    : command

@OutputParam   : Opens Google Search

'''

def web_search(command):

    if not command:
        return

    query = command.lower().strip()

    # Remove command words
    if query.startswith("search for"):
        query = query.replace(
            "search for",
            "",
            1
        ).strip()

    elif query.startswith("search"):
        query = query.replace(
            "search",
            "",
            1
        ).strip()

    if not query:
        asyncio.run(
            speak("Please tell me what to search.")
        )
        return

    search_url = (
        "https://www.google.com/search?q="
        + urllib.parse.quote(query)
    )

    try:

        webbrowser.open(search_url)

        asyncio.run(
            speak(f"Searching for {query}")
        )

    except Exception as e:

        print(f"Search Error: {e}")

        asyncio.run(
            speak("Unable to perform web search.")
        )