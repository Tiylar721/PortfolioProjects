import os
from time import sleep
import datetime 
import pyttsx3
import speech_recognition as sr
import webbrowser as wb
import subprocess
import wikipedia
import pyjokes

#intitialize pyttsx3 engine and set voice and speed

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
voicespeed = 170
engine.setProperty('rate', voicespeed)


#take audio string and speak it using pyttsx3 engine

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#use speech_recognition library to listen to audio from microphone

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognising...")
        query = r.recognize_google(audio, language='en-us')
    except Exception as e:
        print(e)
        speak("Could you please say that again")
        return "None"
    return query

text = get_audio()

if "hello" in text:
    speak("hello, how are you doing today?")
elif "what is your name" in text:
    speak("My name is Dexter")

def time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)

    speak("the current date is")
    speak(year)
    speak(date)
    speak(year)



def wishme():
    speak("Welcome back sir")

    hour = datetime.datetime.now().hour
    if hour >= 4 and hour <= 12:
        speak('Good morning')
    elif hour >=12 and hour <= 18:
        speak('Good afternon')
    elif hour >= 18 and hour <= 24:
        speak('Good evening')
    else:
        speak('Good night')

    speak('How may I assist you today')


if __name__ == "__main__":
    while True:
        query = get_audio().lower()
        print(query)

        if "good morning" in query:
            speak("good morning sir")
            
        elif "time" in query:
            time()
        
        elif "date" in query:
            date()

        elif "offline" in query:
            speak("going offline")
            quit()

        elif "open notepad" in query:
            speak("opening notepad")
            location = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\Notepad.lnk"
            notepad = subprocess.Popen(location)

        elif "close notepad" in query:
            speak("closing notepad")
            notepad.terminate()

        elif "wikipedia" in query:
            speak("searching..")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences = 2)
            speak(result)

        elif "search" in query:
            speak("what would you like me to search?")
            chromepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"
            search = get_audio().lower()
            wb.get(chromepath).open_new_tab(search + ".com")

        elif "joke" in query:
            speak(pyjokes.get_jokes())

        elif "logout" in query:
            speak('logging out in 5 seconds')
            sleep(5)
            os.system("shutdown - 1")

        elif "shutdown" in query:
            speak('shutting down in 5 seconds')
            sleep(5)
            os.system("shutdown /s /t 1")

        elif "restart" in query:
            speak('restarting in 5 seconds')
            sleep(5)
            os.system("shutdown /r /t 1")

        
