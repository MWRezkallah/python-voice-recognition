# app for speech recognition

import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

"""
sapi5 - SAPI5 on Windows
nsss - NSSpeechSynthesizer on Mac OS X
espeak - eSpeak on every other platform
"""
engine = pyttsx3.init("espeak")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.now().hour)
    """
    12:00 - noon
    1:00 pm - morning / 13:00 - afternoon
    18:00 - evening
    """
    if hour >= 0 and hour <= 12:
        speak("Good Morning my dear friend")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon my dear friend")
    else:
        speak("Good evening my dear friend")
    speak("Let me know how can I help you with"
          ", What are you looking for?")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        print("first")
        print("Listening to you Mina ....")
        speak("how can I help you Mina!")
        r.pause_threshold = 0.5
        speak("start talking!")
        audio = r.listen(mic)
        print("audio",audio)
    print("Recognizing your voice....")
    speak("Recognizing your voice Mina!")
    query = r.recognize_google(audio, language="en-US")
    try:
        print(f"My dear friend you said : {query}\n")
    except Exception as e:
        print("Mina say that again please...")
        return "None"
    return query


def sendmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(os.environ["SYSTEM_EMAIL"], os.environ["SYSTEM_EMAIL_PASSWORD"])
    server.sendmail(os.environ["SYSTEM_EMAIL"], to, content)
    server.close()


if __name__ == '__main__':
    
    wishme()

    while True:
        
        query = takecommand().lower()
        
        if 'open wikipedia' in query:
            speak("Searching wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        
        elif 'open brave' in query:
            npath = '/snap/bin/brave'
            os.open(npath)
        
        elif 'open vscode' in query:
            npath = '/snap/bin/code'
            os.open(npath)
        
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
        
        elif 'tell me the time' in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            speak(f"My dear friend, the time is {strTime}")
        
        elif 'open linkedin' in query:
            webbrowser.open("https://www.linkedin.com")
        
        elif 'email to friend' in query:
            try:
                speak("What should I send?")
                content = takecommand()
                to = os.environ["USER_EMAIL"]
                sendmail(to, content)
                speak("Your mail has been sent successfully!")
            except Exception as e:
                print(e)
                speak("My dear friend, ..."\
                    " I'm unable to send the mail"\
                        "please address the error")
        
        else:
            print("could hear anything bye...bye")
            speak("couldn't hear anything bye...bye!")
            break