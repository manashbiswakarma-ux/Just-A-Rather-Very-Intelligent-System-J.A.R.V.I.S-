import datetime

def greetMe(speak):
    hour = int(datetime.datetime.now().hour)
    
    if hour >= 0 and hour < 12:
        greeting = "Good Morning, sir."
    elif hour >= 12 and hour < 18:
        greeting = "Good Afternoon, sir."
    else:
        greeting = "Good Evening, sir."
        
    speak(greeting)