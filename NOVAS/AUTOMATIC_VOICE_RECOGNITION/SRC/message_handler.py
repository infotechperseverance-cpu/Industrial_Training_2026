'''
@Module Name : message_handler.py

@Description : This module contains common helper functions used
               by the File & Folder Management module. It provides
               common voice messages and operation status handling.

@InputParam  : Message

@OutputParam : Status / Voice Response

@Author      : Bhoomi Sapke
'''

from voice import speak
from config import ASSISTANT_NAME
import asyncio

def success(message):
    '''
    Displays and speaks a success message.
    '''
    print(f"{ASSISTANT_NAME}: {message}")
    asyncio.run(speak(message))


def error(message):
    '''
    Displays and speaks an error message.
    '''
    print(f"{ASSISTANT_NAME}: {message}")
    asyncio.run(speak(message))


def information(message):
    '''
    Displays and speaks an information message.
    '''
    print(f"{ASSISTANT_NAME}: {message}")
    asyncio.run(speak(message))


def confirm(message):
    '''
    Displays and speaks a confirmation message.
    '''
    print(f"{ASSISTANT_NAME}: {message}")
    asyncio.run(speak(message))


def ask(message):
    '''
    Asks the user for required information.
    '''
    print(f"{ASSISTANT_NAME} : {message}")
    asyncio.run(speak(message))