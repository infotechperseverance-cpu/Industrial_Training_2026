'''
@Module Name : reminder.py

@Description : This module manages reminder tasks by scheduling,
               storing and monitoring reminders. It processes
               reminder-related commands received from the
               command_processing module.

@Input Param : Voice commands

@Output Param: Reminder notifications

@Author      : Bhoomi Sapke
'''

import asyncio
import threading
import time
import re
import dateparser
from datetime import datetime
from plyer import notification
from database import get_connection
from voice import speak

from message_handler import (
    ask,
    error,
    success,
    information,
    confirm
)


CANCEL_COMMANDS = [
    "cancel",
    "exit",
    "back",
    "go back",
    "go to sleep",
    "close reminder"
]


def get_voice_input(message):
    '''
    Speaks a message and listens for user input.
    Returns None if user cancels.
    '''
    from voice_recognition import speech

    ask(message)

    text = speech()

    if not text:
        return None

    text = text.lower().strip()

    if text in CANCEL_COMMANDS:

        confirm("Reminder cancelled.")

        return None

    return text


def schedule_task():

    from voice_recognition import speech

    ask(
        "Please tell your reminder along with the date and time. "
        "For example, say: "
        "Remind me to attend the meeting tomorrow at 9 A M."
    )

    command = speech()

    if not command:
        error("No reminder received.")
        return

    command = command.lower().strip()
  
    if command in CANCEL_COMMANDS:
        success("Reminder cancelled.")
        return

    # Extract date and time
    reminder_datetime = dateparser.parse(
        command,
        settings={
            "PREFER_DATES_FROM": "future"
        }
    )

    if reminder_datetime is None:

        error("I couldn't understand the reminder time.")
        return

    # Remove common reminder words from task
    task = command

    words = [
        "remind me to",
        "remind me",
        "set reminder",
        "remember to",
        "tomorrow",
        "today",
        "at",
        "on"
    ]

    for word in words:
        task = task.replace(word, "")

    # Remove detected date/time text
    task = re.sub(
        r"\b\d{1,2}(:\d{2})?\s?(am|pm)?\b",
        "",
        task,
        flags=re.IGNORECASE
    )

    task = task.strip()

    if not task:
        task = "Reminder"

    db = None
    cursor = None

    try:

        db = get_connection()
        db = get_connection()

        if db is None:
            print("Database connection failed.")
            return
    

        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO schedule_task
            (
                task_name,
                task_date,
                task_time
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                task,
                reminder_datetime.strftime("%Y-%m-%d"),
                reminder_datetime.strftime("%H:%M:%S")
            )
        )

        db.commit()

        success(
            f"Reminder set for {reminder_datetime.strftime('%d %B %Y %I:%M %p')}"
        )

        

    except Exception as e:

        print(f"Reminder Error: {e}")

        error("Unable to save reminder.")

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


def process(command):


    command = command.lower().strip()

    keywords = [
        "set reminder",
        "reminder",
        "remind me",
        "schedule reminder",
        "add reminder"
    ]

    for keyword in keywords:
        if keyword in command:
            schedule_task()
            return True

    return False



'''
@Function Name : reminder_checker

@Description   : Continuously checks the database for pending
                 reminders. When the scheduled date and time
                 are reached, it notifies the user and updates
                 the reminder status.

@Input Param   : None

@Output Param  : Desktop notification and voice reminder.

@Author        : Bhoomi Sapke
'''

def reminder_checker():

    while True:

        try:

            db = get_connection()

            db = get_connection()

            if db is None:
                print("Database connection failed.")
                time.sleep(5)
                continue

            cursor = db.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    task_name,
                    task_date,
                    task_time,
                    status
                FROM schedule_task
                WHERE
                    CONCAT(task_date,' ',task_time) <= NOW()
                    AND status='Pending'
                """
            )

            reminders = cursor.fetchall()

            for reminder in reminders:

                reminder_id = reminder[0]
                task_name = reminder[1]

                information("Reminder Triggered.")

                notification.notify(
                    title="NOVA Reminder",
                    message=task_name,
                    timeout=10
                )

                asyncio.run(
                    speak(
                        f"Reminder. {task_name}"
                    )
                )

                cursor.execute(
                    """
                    UPDATE schedule_task
                    SET status='Completed'
                    WHERE id=%s
                    """,
                    (reminder_id,)
                )

                db.commit()

            cursor.close()
            db.close()

        except Exception as e:

            print("Reminder Error :", e)

        time.sleep(5)



'''
@Function Name : start_reminder_service

@Description   : Starts the background reminder checking thread.

@Input Param   : None

@Output Param  : None

@Author        : Bhoomi Sapke
'''

def start_reminder_service():

    thread = threading.Thread(
        target=reminder_checker,
        daemon=True
    )

    thread.start()