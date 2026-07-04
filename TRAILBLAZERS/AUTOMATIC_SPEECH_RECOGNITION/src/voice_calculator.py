
import csv
import os
import asyncio
import edge_tts
import pygame
import uuid

#---Store number words and their values
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
     
    "eleven":11,
    "twelve":12,
    "thirteen":13,
    "fourteen":14,
    "fifteen":15,
    "sixteen":16,
    "seventeen":17,
    "eighteen":18,
    "nineteen":19,

    "twenty":20,
    "thirty":30,
    "forty":40,
    "fifty":50,
    "sixty":60,
    "seventy":70,
    "eighty":80,
    "ninety":90,

    "hundred":100

}
#---Store operator words and symbols
opratormap= {

    "plus": "+",
    "minus": "-",
    "times": "*",
    "multiply": "*",
    "into": "*",
    "divided": "/",
    "divide": "/"
}
#---Convert number words into digits
def words_to_number(words):

    total = 0
    current = 0
    
    for word in words:    # If the word is a valid number

        if word in numbermap:

            value = numbermap[word]

            if value == 100:      # Handle the word "hundred"

                if current == 0:
                    current = 1

                current = current * 100

            else:

                current = current + value

    total = total + current

    return str(total)

#---Convert text into a mathematical expression
def convert_to_expression(text):

    words = text.lower().split()

    expression = []

    number_words = []

    for word in words:
        
        if word in numbermap:

            number_words.append(word)
        
        elif word in opratormap:

            if number_words:

                number = words_to_number(number_words)

                expression.append(number)

                number_words.clear()

            expression.append(opratormap[word])
        
        else:
       
            print("Invalid word :", word)

            return None
    #---Add remaining number
    if number_words:

        number = words_to_number(number_words)

        expression.append(number)

    return " ".join(expression)
#---Check whether the expression is valid
def validateExpression(expression):

    try:
        eval(expression)
        return True

    except:
        return False

#---Calculate the result
def calculate_expression(expression):

    result = eval(expression)

    return result

#---Speak the result
async def speak_result(text):

    file_name = str(uuid.uuid4()) + ".mp3"

    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")   # Convert text to speech

    await communicate.save(file_name)

    pygame.mixer.init()

    pygame.mixer.music.load(file_name)

    pygame.mixer.music.play()
    # Wait speech is completed
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(1)

    pygame.mixer.music.unload()

    os.remove(file_name)

#----Save calculation history into CSV file
def save_history(expression, result):

    file = open("history.csv", "a", newline="")

    writer = csv.writer(file)

    writer.writerow([expression, result])

    file.close()
#--Display calculation history
def show_history():
                                                                                                                                                                                                   
    try:

        file = open("history.csv", "r")

        reader = csv.reader(file)


        print("\n\n------ Calculation History ------\n\n")

        for row in reader:
            print(row[0], "=", row[1])

        file.close()

    except Exception:

        print("No History Found.")    

#---Main function 
def main():
    print("\n\n======Voice_Calculater=======\n\n")
    voice_text = input("Enter mathematical expression: ")

    expression = convert_to_expression(voice_text)

    if expression is None:
        print("Invalid Input")
        return

    print("Expression :", expression)

    if validateExpression(expression):

        print("Expression is Valid")

        result = calculate_expression(expression)

        print("Result :", result)

        asyncio.run(speak_result("The answer is " + str(result)))

        save_history(expression, result)

    else:

        print("Error : Invalid Mathematical Expression")

    choice = input("\nDo you want to see calculation history? (yes/no): ")

    if choice.lower() == "yes":
        show_history()
    else:
        print("Thank You!")    

#--Program starts from here
if __name__ == "__main__":
    main()    