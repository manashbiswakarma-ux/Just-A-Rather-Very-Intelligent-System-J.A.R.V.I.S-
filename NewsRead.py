import requests
import json
import pyttsx3
import platform
import time
import speech_recognition as sr

# Initialize pyttsx3 TTS engine based on OS
system = platform.system()
if system == 'Windows':
    engine = pyttsx3.init('sapi5')
elif system == 'Darwin':  # macOS
    engine = pyttsx3.init('nsss')
else:
    engine = pyttsx3.init('espeak')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say the news category you want: business, entertainment, health, science, sports, technology")
        print("Listening for news category...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
    try:
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except Exception as e:
        speak("Sorry, I did not catch that. Please try again.")
        print("Error recognizing speech:", e)
        return None

api_key = "75a0fbf3c05a4a86aae041f92483d0fe"

def latestnews():
    api_dict = {
    "business": f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={api_key}",
    "entertainment": f"https://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey={api_key}",
    "health": f"https://newsapi.org/v2/top-headlines?country=us&category=health&apiKey={api_key}",
    "science": f"https://newsapi.org/v2/top-headlines?country=us&category=science&apiKey={api_key}",
    "sports": f"https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey={api_key}",
    "technology": f"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={api_key}"
    }


   
    field = listen_command()
    if not field:
        return


    selected_category = None
    for key in api_dict.keys():
        if key in field:
            selected_category = key
            break

    if not selected_category:
        speak("Sorry, I don't have news for that category. Please try again.")
        print("Category not recognized:", field)
        return

    url = api_dict[selected_category]

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        speak("Sorry, I couldn't get the news due to a connection error.")
        print("Error fetching news:", e)
        return

    if data.get("status") != "ok":
        speak(f"Sorry, failed to get news. Message from server: {data.get('message', 'No message')}")
        print("API error:", data)
        return

    articles = data.get("articles", [])
    if not articles:
        speak(f"Sorry, there are no news articles available for {selected_category} right now.")
        return

    speak(f"Here are the top {len(articles)} {selected_category} news headlines.")

    for idx, article in enumerate(articles, 1):
        title = article.get("title")
        if title:
            print(f"{idx}. {title}")
            speak(title)
            time.sleep(1)

            cont = input("Press 1 to continue or 2 to stop: ").strip()
            if cont == "2":
                speak("Okay, stopping the news now.")
                break

    speak("That's all for now. Have a nice day!")

if __name__ == "__main__":
    latestnews()
