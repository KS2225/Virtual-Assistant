import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import *
import time
from datetime import date
import wikipedia
import pywhatkit
import pyjokes
# importing library
import requests
from bs4 import BeautifulSoup

def weather_forecast():
    res = requests.get('https://ipinfo.io/')
    # Receiving the response in JSON format
    data = res.json()
    # Extracting the Location of the City from the response
    city = data['city']

    # creating url and requests instance
    url = "https://www.google.com/search?q="+"weather"+city
    html = requests.get(url).content

    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    temp = temp.split("°")
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

    # formatting data
    data = str.split('\n')
    time = data[0]
    sky = data[1]

    # getting all div tag
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text

    # getting other required data
    pos = strd.find('Winds')
    other_data = strd[pos:]
    final = " Temperature is"+temp[0] +" degrees Celsius at Time:"+ time+ " There is" +sky
    # printing all data
    return final
recognizer = sr.Recognizer()
microphone = sr.Microphone()

engine = pyttsx3.init()
engine.setProperty('volume', 1.0, )
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
WAKE = "Friday"



search_words = { "when": "when", "where": "where", "why": "why", "how": "how"}

class Kshati:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def hear(self, recognizer, microphone, response):
        try:
            with microphone as source:
                print("Waiting for command...")
                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000
                audio = recognizer.listen(source, timeout= 7.0)
                command = recognizer.recognize_google(audio)
                print(command)
#                 k.remember(command)
                return command.lower()
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Network Error!")

            

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

            
    def find_search_words(self, command):
        if search_words.get(command.split(' ')[0]) == command.split(' ')[0]:
            return True
        else:
            return False
    
    def analyze(self,command):
        try:
            if "today's date" in command:
                k.speak(date.today())
            elif "the time" in command:
                date_time = time.strftime("%I:%M %p")
                k.speak(date_time)
            elif "weather" in command:
                k.speak(weather_forecast())
            elif "who is" in command:
                person = command.replace('who is', '')
                info = wikipedia.summary(person,1, auto_suggest= False)
                k.speak(info)
            elif "what is" in command:
                subject = command.replace('what is', '')
                info = wikipedia.summary(subject,2, auto_suggest= False)
                k.speak(info)
            elif "joke" in command:
                k.speak(pyjokes.get_joke())
            elif self.find_search_words(command):
                k.speak("Here is what I found...")
                webbrowser.open("https://www.google.com/search?q={}".format(command))
            elif 'play' in command:
                song = command.replace('play', '')
                k.speak('playing ' + song)
                pywhatkit.playonyt(song)
            
            elif command == "open youtube":
                webbrowser.open("https://www.youtube.com/")
                k.speak("Opening YouTube")
            elif command == "open chats":
                webbrowser.open("https://web.whatsapp.com/")
                k.speak("Opening WhatsApp")
            elif command == "open mail":
                webbrowser.open("https://mail.google.com/mail/")
                k.speak("Opening Gmail")
            elif command == "introduce yourself":
                k.speak("My name is Friday. I am a Virtual Assistant.")
            else:
                k.speak("I don't know how to do that yet.")
        except TypeError:
            pass
        
    def listen(self, recognizer, microphone):
        while True:
            try:
                with microphone as source:
                    print("Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.dynamic_energy_threshold = 3000
                    audio = recognizer.listen(source, timeout=7.0)
                    response = recognizer.recognize_google(audio)
                    if response == WAKE:
                        k.speak("How can I help you?")
                        print(response)
                        return response.lower()
                    else:
                        pass
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Network Error!")
k = Kshati()
k.speak("Hello! I am Friday. Holler my name, if you need any help!")
# k.start_conversation_log()
while True:
    response = k.listen(recognizer, microphone)
    command = k.hear(recognizer, microphone, response)
    k.analyze(command)
