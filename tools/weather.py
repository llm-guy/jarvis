# tools/weather.py

from langchain.tools import tool
import requests
import os

@tool
def get_weather(city: str) -> str:
    """Get current weather information for a city."""
    try:
        # You can get a free API key from openweathermap.org
        api_key = os.getenv("OPENWEATHER_API_KEY")
        
        if not api_key:
            return "Weather service not configured. Please set OPENWEATHER_API_KEY environment variable."
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            
            return f"Weather in {city}: {description}, {temp}°C (feels like {feels_like}°C), humidity {humidity}%"
        else:
            return f"Could not get weather for {city}. Please check the city name."
            
    except Exception as e:
        return f"Weather service error: {e}"
