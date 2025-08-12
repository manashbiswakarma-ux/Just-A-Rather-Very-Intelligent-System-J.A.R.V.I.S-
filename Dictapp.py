import os
import pyautogui
import webbrowser
import pyttsx3
import platform
import subprocess
from time import sleep

# Detect OS
system = platform.system()

# Setup TTS Engine
if system == 'Windows':
    engine = pyttsx3.init('sapi5')
elif system == 'Darwin':  # macOS
    engine = pyttsx3.init('nsss')
else:
    engine = pyttsx3.init('espeak')  # Linux

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Absolute macOS app paths
dictapp_mac = {
    "safari": "/Applications/Safari.app",
    "notes": "/Applications/Notes.app",
    "calendar": "/Applications/Calendar.app",
    "finder": "/System/Library/CoreServices/Finder.app",
    "spotify": "/Applications/Spotify.app",
    "vscode": "/Applications/Visual Studio Code.app",
    "chrome": "/Applications/Google Chrome.app",
    "messages": "/Applications/Messages.app",
    "facetime": "/Applications/FaceTime.app",
    "mail": "/Applications/Mail.app",
    "photos": "/Applications/Photos.app",
    "reminders": "/Applications/Reminders.app",
    "preview": "/Applications/Preview.app",
    "music": "/Applications/Music.app"
}

# Generic app commands for fallback (Windows / Linux / CLI use)
dictapp = {
    "commandprompt": "cmd" if system == 'Windows' else "Terminal",
    "paint": "mspaint" if system == 'Windows' else "Paintbrush",
    "word": "winword" if system == 'Windows' else "Microsoft Word",
    "excel": "excel" if system == 'Windows' else "Microsoft Excel",
    "chrome": "chrome" if system == 'Windows' else "Google Chrome",
    "vscode": "code" if system == 'Windows' else "Visual Studio Code",
    "powerpoint": "powerpnt" if system == 'Windows' else "Microsoft PowerPoint",
}

def openappweb(query):
    speak("Launching, sir")
    query = query.lower()

    # If it's a website
    for domain in [".com", ".co.in", ".org", ".net", ".edu"]:
        if domain in query:
            clean_query = query.lower()
            for word in ["open", "launch", "jarvis", "please", " "]:
                clean_query = clean_query.replace(word, "")
            if not clean_query.startswith("http"):
                clean_query = "https://www." + clean_query
            webbrowser.open(clean_query)
            return

    # Try macOS absolute apps
    if system == 'Darwin':
        for key in dictapp_mac:
            if key in query:
                subprocess.call(["open", dictapp_mac[key]])
                return

    # Try fallback dictapp
    for key in dictapp:
        if key in query:
            if system == 'Windows':
                os.system(f"start {dictapp[key]}")
            elif system == 'Darwin':
                subprocess.call(["open", "-a", dictapp[key]])
            else:
                subprocess.call([dictapp[key]])
            return

    speak("Sorry, I couldn't find that app.")


def closeappweb(query):
    speak("Closing, sir")
    query = query.lower()

    # Close specific tabs
    tab_map = {
        "1 tab": 1, "one tab": 1,
        "2 tab": 2, "two tab": 2,
        "3 tab": 3, "three tab": 3,
        "4 tab": 4, "four tab": 4,
        "5 tab": 5, "five tab": 5
    }

    for key, count in tab_map.items():
        if key in query:
            for _ in range(count):
                pyautogui.hotkey("command" if system == 'Darwin' else "ctrl", "w")
                sleep(0.5)
            speak("Closed tabs")
            return

    # Close apps
    for key in dictapp_mac if system == 'Darwin' else dictapp:
        if key in query:
            if system == 'Windows':
                os.system(f"taskkill /f /im {dictapp[key]}.exe")
            elif system == 'Darwin':
                subprocess.call(['osascript', '-e', f'quit app "{key.capitalize()}"'])
            else:
                subprocess.call(["pkill", "-f", dictapp[key]])
            speak(f"{key.capitalize()} closed")
            return

    speak("App not found to close.")
