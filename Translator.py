import platform
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from playsound import playsound
import pyttsx3
import os
import time

# Initialize text-to-speech engine based on OS
system = platform.system()
if system == 'Windows':
    engine = pyttsx3.init('sapi5')
elif system == 'Darwin':  # macOS
    engine = pyttsx3.init('nsss')
else:
    engine = pyttsx3.init('espeak')  # Linux

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception:
        print("Sorry, I didn't get that. Please say that again.")
        return "None"
    return query

def get_lang_code(lang_input):
    lang_input = lang_input.lower().strip()
    if lang_input in LANGUAGES:
        return lang_input
    for code, name in LANGUAGES.items():
        if lang_input == name.lower():
            return code
def translategl(query):
    speak("Sure, I can translate that.")
    speak("Please say the name of the language you want to translate to.")
    
    lang_input = take_command()
    
    if lang_input == "None":
        speak("I didn't hear a language. Please try again.")
        return

    lang_code = get_lang_code(lang_input)
    if not lang_code:
        speak(f"Sorry sir, I could not find the language {lang_input}.")
        print("Invalid language input.")
        return

    translator = Translator()
    try:
        translated = translator.translate(query, src="auto", dest=lang_code)
        text = translated.text
        dest_lang_name = LANGUAGES.get(lang_code, "the selected language")
        
        print(f"Translated to {dest_lang_name}: {text}")
        speak(f"In {dest_lang_name}, that is: {text}")

        # The following part uses gTTS to speak in the translated language
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save("translated_voice.mp3")
        playsound("translated_voice.mp3")
        time.sleep(2)
        os.remove("translated_voice.mp3")
        
    except Exception as e:
        # MOD: More detailed error printing
        print("\n--- DETAILED ERROR ---")
        print(f"An error occurred: {e}")
        print(f"Error Type: {type(e).__name__}")
        print("This could be due to an unsupported language for speech, a network issue, or the googletrans library.")
        print("----------------------\n")
        speak("Sorry sir, an error occurred during the translation.")

if __name__ == "__main__":
    speak("Hello sir, what would you like me to translate?")
    query = take_command()
    if query != "None":
        translategl(query)
    else:
        speak("No input detected, exiting.")
