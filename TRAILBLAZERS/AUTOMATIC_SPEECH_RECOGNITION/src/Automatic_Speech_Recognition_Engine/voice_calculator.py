"""
=========================================
Voice Calculator Module
Purpose:
Perform mathematical calculations using voice commands.
=========================================
"""

import json
import os
from datetime import datetime

from voice_engine import speak
from speech_recognition_module import listen
from commandHistory import save_command


# ---------- Number Dictionary ----------
numbermap = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,

    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,

    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,

    "hundred": 100,
    "thousand": 1000
}


# ---------- Operator Dictionary ----------
operatormap = {

    "plus": "+",
    "add": "+",

    "minus": "-",
    "subtract": "-",

    "times": "*",
    "multiply": "*",
    "multiplied": "*",
    "into": "*",
    "x": "*",

    "divide": "/",
    "divided": "/",
    "over": "/",

    "mod": "%",
    "modulus": "%",

    "power": "**"
}


# ---------- Convert Number Words ----------
def words_to_number(words):

    total = 0
    current = 0

    for word in words:

        if word not in numbermap:
            continue

        value = numbermap[word]

        if value == 100:

            if current == 0:
                current = 1

            current *= 100

        elif value == 1000:

            if current == 0:
                current = 1

            total += current * 1000
            current = 0

        else:

            current += value

    total += current

    return str(total)


# ---------- Convert Voice/Text into Expression ----------
def convert_to_expression(text):

    if text is None:
        return None

    text = text.lower().strip()

    # Remove filler words
    fillers = [
        "calculate",
        "what is",
        "please",
        "answer",
        "equals",
        "equal to",

    ]

    for item in fillers:
        text = text.replace(item, "")

    text = text.strip()

    # If user already spoke an expression like:
    # 5+6
    # 100/25
    # 12*9
    try:
        eval(text, {"__builtins__": None}, {})
        return text

    except Exception:
        pass

    words = text.split()

    expression = []
    number_words = []

    for word in words:

        if word in numbermap:

            number_words.append(word)

        elif word in operatormap:

            if number_words:

                expression.append(words_to_number(number_words))
                number_words.clear()

            expression.append(operatormap[word])

        else:

            print("Invalid Word :", word)
            return None

    if number_words:

        expression.append(words_to_number(number_words))

    return " ".join(expression)


# ---------- Validate Expression ----------
def validateExpression(expression):

    if expression is None:
        return False

    try:

        eval(expression, {"__builtins__": None}, {})

        return True

    except Exception:

        return False


# ---------- Calculate ----------
def calculate_expression(expression):

    return eval(expression, {"__builtins__": None}, {})


# ---------- Speak Result ----------
def speak_result(result):

    speak(f"The answer is {result}")


# ---------- Calculator History ----------
HISTORY_FILE = "calculator_history.json"


# ---------- Save History ----------
def save_history(expression, result):

    try:

        if os.path.exists(HISTORY_FILE):

            with open(HISTORY_FILE, "r") as file:

                history = json.load(file)

        else:

            history = []

    except Exception:

        history = []

    history.append({

        "expression": expression,

        "result": result,

        "date": datetime.now().strftime("%d-%m-%Y"),

        "time": datetime.now().strftime("%H:%M:%S")

    })

    try:

        with open(HISTORY_FILE, "w") as file:

            json.dump(history, file, indent=4)

    except Exception as e:

        print(e)


# ---------- Show History ----------
def show_history():

    try:

        with open(HISTORY_FILE, "r") as file:

            history = json.load(file)

        if len(history) == 0:

            print("No History Found.")
            speak("No calculation history found.")
            return

        print("\n========== Calculator History ==========\n")

        for item in history:

            print(
                f"{item['expression']} = {item['result']} | "
                f"{item['date']} {item['time']}"
            )

    except Exception:

        print("No History Found.")
        speak("No calculation history found.")


# ---------- Clear History ----------
def clear_history():

    try:

        with open(HISTORY_FILE, "w") as file:

            json.dump([], file, indent=4)

        print("Calculator history cleared.")

        speak("Calculator history cleared.")

    except Exception as e:

        print(e)

        speak("Unable to clear calculator history.")

# ---------- Process Calculation ----------
def process_calculation(voice_text):

    if voice_text is None or voice_text.strip() == "":

        print("Invalid mathematical expression.")
        speak("Invalid mathematical expression.")
        save_command("Voice Calculator", "Failed")
        return None

    expression = convert_to_expression(voice_text)

    if expression is None:

        print("Invalid mathematical expression.")
        speak("Invalid mathematical expression.")
        save_command("Voice Calculator", "Failed")
        return None

    if not validateExpression(expression):

        print("Invalid mathematical expression.")
        speak("Invalid mathematical expression.")
        save_command("Voice Calculator", "Failed")
        return None

    try:

        result = calculate_expression(expression)

        print("\n========== Voice Calculator ==========")
        print("Expression :", expression)
        print("Result     :", result)
        print("======================================")

        speak_result(result)

        save_history(expression, result)

        save_command("Voice Calculator", "Success")

        return result

    except ZeroDivisionError:

        print("Division by zero is not allowed.")

        speak("Division by zero is not allowed.")

        save_command("Voice Calculator", "Failed")

        return None

    except Exception as e:

        print(e)

        speak("Calculation failed.")

        save_command("Voice Calculator", "Failed")

        return None


# ---------- Start Voice Calculator ----------
def start_voice_calculator():

    print("\n===================================")
    print("      VOICE CALCULATOR")
    print("===================================\n")

    speak("Voice calculator started.")
    speak("Please speak your mathematical expression.")

    while True:

        voice_text = listen()

        if voice_text is None:

            speak("I did not understand. Please try again.")
            continue

        voice_text = voice_text.lower().strip()

        # Exit Calculator
        if voice_text in [
            "exit",
            "stop",
            "close",
            "close calculator",
            "exit calculator"
        ]:

            speak("Closing voice calculator.")
            return

        # Show History
        if voice_text in [
            "history",
            "show history",
            "calculator history"
        ]:

            show_history()
            continue

        # Clear History
        if voice_text in [
            "clear history",
            "delete history",
            "remove history"
        ]:

            clear_history()
            continue

        process_calculation(voice_text)

def is_math_command(text):

    if text is None:
        return False

    text = text.lower()

    math_words = [
        "plus",
        "minus",
        "times",
        "multiply",
        "multiplied",
        "divide",
        "divided",
        "over",
        "mod",
        "modulus",
        "power",
        "add",
        "subtract",
        "into"
    ]

    math_symbols = ["+", "-", "*", "/", "%", "**"]

    if any(symbol in text for symbol in math_symbols):
        return True

    words = text.split()

    for word in words:
        if word in numbermap:
            return True

        if word in math_words:
            return True

    return False