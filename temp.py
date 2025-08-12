import datetime
import webbrowser
import pyttsx3
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import os
import pyautogui
import random
from plyer import notification
from pygame import mixer
import speedtest
import platform
import threading
import eel

from Calculatenumbers import calc
from weather import get_weather
from Dictapp import openappweb, closeappweb
from gemini import ask_gemini
from GreetMe import greetMe

eel.init('www')

is_awake = False
tts_lock = threading.Lock()

system = platform.system()
if system == 'Windows':
    engine = pyttsx3.init('sapi5')
else:
    engine = pyttsx3.init('nsss')

voices = engine.getProperty("voices")
engine.setProperty("voice",'com.apple.voice.compact.en-GB.Daniel')
engine.setProperty("rate", 170)

def speak(audio):
    with tts_lock:
        eel.update_jarvis_response(audio)
        engine.say(audio)
        engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        eel.update_status("Listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=5)
            eel.update_status("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            eel.update_user_query(query)
            return query.lower()
        except Exception:
            if is_awake:
                eel.update_status("Ready")
            else:
                eel.update_status("Sleeping")
            return ""

password = "7636815699" 
def process_command(query):
    global is_awake
    if not query:
        if is_awake:
            eel.update_status("Ready")
        else:
            eel.update_status("Sleeping")
        return

    if not is_awake:
        if "wake up" in query:
            is_awake = True
            greetMe()
            eel.update_status("Ready")
            eel.showSiriWave()()
        else:
            speak("I am sleeping. Please say wake up to continue.")
            eel.update_status("Sleeping")
        return

    if "go to sleep" in query:
        speak("Understood. Going to sleep.")
        is_awake = False
        eel.update_status("Sleeping")
        eel.hideSiriWave()()

    elif "open" in query or "launch" in query:
        openappweb(query)
    elif "close" in query or "quit" in query:
        closeappweb(query)
    elif "google" in query:
        from SearchNow import searchGoogle
        searchGoogle(query)
    elif "youtube" in query:
        from SearchNow import searchYoutube
        searchYoutube(query)
    elif "wikipedia" in query:
        from SearchNow import searchWikipedia
        searchWikipedia(query)
    elif "change password" in query:
        speak("For security, passwords can only be changed through a dedicated form in the user interface.")
    elif "schedule my day" in query:
        speak("This feature requires a user interface form to add tasks. I cannot do it via voice command in this version.")
    elif "show my schedule" in query:
        try:
            with open("tasks.txt", "r") as file:
                content = file.read()
            if content.strip():
                notification.notify(title="My Schedule", message=content, timeout=15)
                speak("Here is the schedule I have on file.")
            else:

                speak("Your schedule is currently empty.")
        except FileNotFoundError:
            speak("I could not find a schedule file.")
    elif "remember that" in query:
        rememberMessage = query.replace("remember that", "").replace("jarvis", "").strip()
        speak(f"You told me to remember that: {rememberMessage}")
        with open("Remember.txt", "a") as remember:
            remember.write(rememberMessage + "\n")
    elif "what do you remember" in query:
        with open("Remember.txt", "r") as remember:
            content = remember.read()
            speak("You told me to remember that: " + content if content else "You haven't asked me to remember anything yet.")
    elif "focus mode" in query:
        speak("Entering focus mode. The main application will close.")
        try:
            os.startfile("FocusMode.py")
            exit()
        except Exception as e:
            speak(f"Could not start focus mode. Error: {e}")
    elif "show my focus" in query:
        from FocusGraph import focus_graph
        focus_graph()
    elif "translate" in query:
        from Translator import translategl
        query = query.replace("jarvis", "").replace("translate", "")
        translategl(query)
    elif "internet speed" in query:
        speak("Testing internet speed. This might take a moment.")
        try:
            wifi = speedtest.Speedtest()
            upload_net = wifi.upload() / 1048576
            download_net = wifi.download() / 1048576
            speak(f"Your download speed is {download_net:.2f} megabits per second.")
            speak(f"And your upload speed is {upload_net:.2f} megabits per second.")
        except Exception:
            speak("I was unable to connect to the speed test server.")
    elif "ipl score" in query:
        try:
            url = "https://www.cricbuzz.com/"
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            team1 = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")[0].get_text()
            team2 = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")[1].get_text()
            team1_score = soup.find_all(class_="cb-ovr-flo")[8].get_text()
            team2_score = soup.find_all(class_="cb-ovr-flo")[10].get_text()
            speak(f"The current score is: {team1}, {team1_score}. And {team2}, {team2_score}.")
        except Exception:
            speak("I'm sorry, I couldn't retrieve the IPL score at this time.")
    elif "screenshot" in query:
        im = pyautogui.screenshot()
        im.save("screenshot.jpg")
        speak("Done. The screenshot is saved as screenshot.jpg.")
    elif "click my photo" in query:
        pyautogui.press("super")
        pyautogui.typewrite("camera")
        pyautogui.press("enter")
        pyautogui.sleep(2)
        speak("Smile!")
        pyautogui.press("enter")
    elif "shutdown system" in query:
        speak("Are you sure you want to shut down? Please say 'confirm shutdown' to proceed.")
        shutdown_confirmation = takeCommand().lower()
        if "confirm shutdown" in shutdown_confirmation:
            speak("Shutting down the system now.")
            if system == "Windows":
                os.system("shutdown /s /t 1")
            else:
                command = f'echo "{password}" | sudo -S shutdown -h now'
                os.system(command)
        else:
            speak("Shutdown cancelled.")
    elif "play a game" in query:
        from game import game_play
        game_play()
    elif "tired" in query:
        speak("Playing a motivating song for you, sir.")
        webbrowser.open("https://www.youtube.com/watch?v=E3jOYQGu1uw")
    elif "pause" in query:
        pyautogui.press("k")
        speak("Paused.")
    elif "play" in query:
        pyautogui.press("k")
        speak("Playing.")
    elif "mute" in query:
        pyautogui.press("m")
        speak("Muted.")
    elif "volume up" in query:
        from keyboard import volumeup
        speak("Volume up.")
        volumeup()
    elif "volume down" in query:
        from keyboard import volumedown
        speak("Volume down.")
        volumedown()
    elif "hello" in query:
        speak("Hello sir, how are you?")
    elif "i am fine" in query:
        speak("That's great to hear.")
    elif "how are you" in query:
        speak("I am fully operational and ready for your command.")
    elif "thank you" in query:
        speak("You're welcome, sir.")
    elif "news" in query:
        from NewsRead import latestnews
        latestnews()
    elif "calculate" in query:
        calc(query)
    elif "whatsapp" in query:
        from Whatsapp import sendMessage
        sendMessage()
    elif "temperature" in query or "weather" in query:
        words = query.split()
        city = "Guwahati"
        if "in" in words:
            try:
                city = words[words.index("in") + 1]
            except IndexError: pass
        result = get_weather(city)
        speak(result)
    elif "set an alarm" in query:
        speak("This feature requires a UI form to set the alarm time. I cannot do it with voice alone.")
    elif "the time" in query:
        strTime = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Sir, the time is {strTime}")
    else:
        ai_reply = ask_gemini(query)
        speak(ai_reply)

    if is_awake:
        eel.update_status("Ready")

@eel.expose
def start_interaction():
    query = takeCommand()
    process_command(query)

if __name__ == "__main__":
    eel.start('index.html', size=(1000, 700), mode='chrome')