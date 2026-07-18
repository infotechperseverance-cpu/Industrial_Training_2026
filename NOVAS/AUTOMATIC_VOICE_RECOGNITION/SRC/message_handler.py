'''
@Module Name : common.py

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
    asyncio.run(print(f"SUCCESS : {message}"))
    asyncio.run(speak(message))


def error(message):
    '''
    Displays and speaks an error message.
    '''
    asyncio.run(print(f"ERROR : {message}"))
    asyncio.run(speak(message))


def information(message):
    '''
    Displays and speaks an information message.
    '''
    asyncio.run(print(f"INFO : {message}"))
    asyncio.run(speak(message))


def confirm(message):
    '''
    Displays and speaks a confirmation message.
    '''
    asyncio.run(print(f"CONFIRM : {message}"))
    asyncio.run(speak(message))


def ask(message):
    '''
    Asks the user for required information.
    '''
    asyncio.run(print(f"{ASSISTANT_NAME} : {message}"))
    asyncio.run(speak(message))