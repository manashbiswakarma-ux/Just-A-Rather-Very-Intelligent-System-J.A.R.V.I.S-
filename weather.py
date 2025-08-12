import requests

def get_weather(city="Guwahati", api_key=""):
    try:
        # Format the city for multi-word inputs (e.g., "New York" → "New+York")
        city = city.strip().replace(" ", "+")

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if data.get("cod") == 200:
            city_name = data["name"]
            country = data["sys"]["country"]
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"The weather in {city_name}, {country} is {weather} with a temperature of {temp}°C."
        else:
            return f"Weather data not found for {city.replace('+', ' ')}: {data.get('message', 'No error message from server')}"
    except Exception as e:
        return f"Could not get weather information. Error: {e}"
