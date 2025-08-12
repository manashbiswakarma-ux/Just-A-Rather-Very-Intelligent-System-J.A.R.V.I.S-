import pyttsx3
import wolframalpha
import platform

# Initialize pyttsx3 engine according to OS
system = platform.system()
if system == 'Windows':
    engine = pyttsx3.init('sapi5')
elif system == 'Darwin':
    engine = pyttsx3.init('nsss')
else:
    engine = pyttsx3.init('espeak')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

import requests

def Wolfram(query):
    api_key = ""
    client = wolframalpha.Client(api_key)
    res = client.query(query)
    try:
        answer = next(res.results).text
        return answer
    except Exception as e:
        print("Error from WolframAlpha:", e)
        return None




import traceback

def calc(query):
    query = query.lower()
    query = query.replace("calculate", "")
    query = query.replace("plus", "+")
    query = query.replace("minus", "-")
    query = query.replace("multiply", "*")
    query = query.replace("times", "*")
    query = query.replace("divide", "/")
    query = query.replace("divided by", "/")
    query = query.strip()

    print(f"Query sent to WolframAlpha: {query}")  # Debugging output

    try:
        result = Wolfram(query)
        if result:
            print(f"Result: {result}")
            speak(result)
        else:
            speak("Sorry sir, I couldn't compute that.")
    except Exception as e:
        print("Error occurred:")
        traceback.print_exc()  # This prints detailed error info
        speak("Sorry sir, I couldn't compute that.")

