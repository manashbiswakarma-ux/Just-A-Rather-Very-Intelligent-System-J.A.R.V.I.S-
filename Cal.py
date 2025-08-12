# Cal.py

import pyttsx3
import platform
import wolframalpha

# Determine the system for pyttsx3 voice engine
system = platform.system()
if system == 'Windows':
    Assistant = pyttsx3.init('sapi5')
elif system == 'Darwin':  # macOS
    Assistant = pyttsx3.init('nsss')
else:
    Assistant = pyttsx3.init('espeak')

voices = Assistant.getProperty('voices')
Assistant.setProperty('voice', voices[0].id)
Assistant.setProperty('rate', 200)

# Speak function
def Speak(audio):
    print(f": {audio}")
    Assistant.say(audio)
    Assistant.runAndWait()

# WolframAlpha query handler
def Wolfram(query):
    api_key = ""  # Use your valid API key
    requester = wolframalpha.Client(api_key)
    requested = requester.query(query)

    try:
        Answer = next(requested.results).text
        return Answer
    except:
        Speak("Sorry sir, the value is not answerable!")
        return None

# Main calculation logic
def calc(query):
    Term = str(query).lower()
    Term = Term.replace("jarvis", "")
    Term = Term.replace("what is", "")
    Term = Term.replace("calculate", "")
    Term = Term.replace("plus", "+")
    Term = Term.replace("minus", "-")
    Term = Term.replace("divide", "/")
    Term = Term.replace("multiplied by", "*")
    Term = Term.replace("multiply", "*")
    Term = Term.replace("x", "*")  # For "10 x 5"
    Term = Term.strip()

    try:
        result = Wolfram(Term)
        if result:
            print(f"Answer: {result}")
            Speak(result)
    except Exception as e:
        print("Error:", e)
        Speak("Sorry sir, the query is not answerable!")
