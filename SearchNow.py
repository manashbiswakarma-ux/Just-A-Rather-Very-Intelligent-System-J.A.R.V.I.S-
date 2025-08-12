import webbrowser
import speech_recognition
import pyttsx3
import pywhatkit
import wikipedia
import platform

system = platform.system()
if system == 'Windows':
    engine = pyttsx3.init('sapi5')
elif system == 'Darwin':  # macOS
    engine = pyttsx3.init('nsss')
else:
    engine = pyttsx3.init('espeak')  # Linux

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)
    
    try:
        print("Understanding....")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query.lower()

def searchGoogle(query):
    if "google" in query:
        query = query.replace("jarvis", "")
        query = query.replace("google search", "")
        query = query.replace("google", "")
        query = query.replace("search on", "")
        speak("This is what I found on Google")
        try:
            pywhatkit.search(query)
            result = wikipedia.summary(query, 1)
            speak(result)
        except:
            speak("No speakable output available")

def searchYoutube(query):
    """
    Searches YouTube and opens the search results page in a browser.
    """
    search_query = query.replace("Youtube", "").replace("youtube", "").replace("jarvis", "").replace("search", "").strip()

    if not search_query:
        speak("What video should I search for on YouTube?")
        return
        
    speak(f"Showing you the Youtube results for {search_query}.")
    
    # Construct the URL for the search results page
    web_url = f"https://www.youtube.com/results?search_query={search_query}"
    
    # Open the URL in the default web browser
    webbrowser.open(web_url)
    


def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from Wikipedia...")
        query = query.replace("wikipedia", "")
        query = query.replace("search wikipedia", "")
        query = query.replace("jarvis", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia...")
        print(results)
        speak(results)
