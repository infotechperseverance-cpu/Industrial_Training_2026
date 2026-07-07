
import smtplib
from email.message import EmailMessage
import speech_recognition as sr
import win32com.client
import re
import os
import csv
from datetime import datetime

#--------Text-to-Speech-------
speaker = win32com.client.Dispatch("SAPI.SpVoice")
def speak(text):
    print(text)
    speaker.Speak(text)

#--------eamil_validation--------
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

#-------Voice Input--------
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        speak("Listening")

        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source,timeout = 20,phrase_time_limit = 30)
        
    try:
        text = recognizer.recognize_google(audio,language = "en-IN")
        speak("You said "+text)
        return text.lower()
    
    except sr.UnknownValueError:
        speak("please speak again")
        return listen()
    
    except:
        speak("I could not understand")
        return ""
    
#---------Email_Sending-----------    
def send_email(receiver,subject,message):
    sender = "bvwagh19@gmail.com"
    password = "kyinoyjpjezxpzct"

    if not is_valid_email(receiver):
        speak("Invalid email address")
        return

    msg = EmailMessage()
    msg["from"] = sender
    msg["to"] = receiver
    msg["subject"] = subject
    msg.set_content(message)
               
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # Login
        server.login(sender,password)
        print("Login Successful")

        server.send_message(msg)
        server.quit()

        save_email_history(receiver, subject, message)

        speak('Email send successfully')

    except Exception as e:
        print("error:",e)
        speak("Failed to send email")

#------------Email_History----------
def save_email_history(receiver, subject, message):
    file_name = "sent_emails.csv"

    file_exists = os.path.isfile(file_name)

    with open(file_name, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Date & Time", "Receiver", "Subject", "Message"])

        writer.writerow([
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            receiver,
            subject,
            message
        ])
   
contacts ={
    "vijay":"vswagh03@gmail.com"
}

#-----------Main Progaram----------
speak("say your command")
command = listen()

if "send email" in command:
     speak("okay,I will send an email")
     speak("whom do you want send email ?")
     name = listen().strip().lower()
     print("Receiver name:",name)

     if name in contacts:
        receiver = contacts[name]

        speak("speak the subject")
        subject = listen()

        speak("speak the message")
        message = listen()
        if len(message.strip()):
            speak("Message captured successfully.")
        else:
            speak("Please speak the complete message again.") 
            message = listen()   

        send_email(receiver, subject, message)

     else:
        speak("Contact not found.")

else:
    speak("Unsupported command.")   






    
        

