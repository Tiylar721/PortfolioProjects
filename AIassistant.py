import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
import time
import pyttsx3
import speech_recognition as sr
import pytz

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]


def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)                            
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said


def authenticate_google():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service

def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    enddate = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId="primary", timeMin=date.isoformat(),
                                          timeMax=end_date.isoformat(), singleEvents=True,
                                           orderBy="startTime").execute()
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
    else:
        speak(f"You have {len(events)} events on this day")

    # Prints the start and name of the next 10 events
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
        start_time = str(start.split("T")[1].split("-")[0])
        if int(start_time.split(":")[0]) < 12:
            start_time = start_time + "am"
        else:
            start_time = str(int(start_time.split(":")[0])-12)
            start_time = start_time + "pm"

        speak(event["summary"] + " at " + start_time) 

def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today
    
    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7
        return today + datetime.timedelta(dif)
    
    if day != -1:
        return datetime.date(month=month, day=day, year=year)

service = authenticate_google()
print("Start")
text = get_audio()

CALENDER_STRS = ["What do I have", "Do I have plans", "Am I busy"]
for phrase in text.lower():
    date = get_date(text)
    if date:
        get_events(date, service)
    else:
        speak("Please try again")