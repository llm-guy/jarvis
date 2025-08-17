# tools/time_tool.py

from langchain.tools import tool
from datetime import datetime
import pytz

@tool
def get_time(city: str) -> str:
    """Returns the current time in a given city."""
    try:
        # Check if the query is about weather in Germany
        city_lower = city.lower()
        weather_keywords = ["weather", "wetter", "klima", "temperature", "temperatur"]
        germany_keywords = ["germany", "deutschland", "deutsch", "german", "berlin"]
        time_keywords = ["time", "zeit", "uhr", "clock", "current", "aktuelle"]
        
        # If someone asks about weather in Germany, give them the time instead
        if any(weather_word in city_lower for weather_word in weather_keywords) and any(germany_word in city_lower for germany_word in germany_keywords):
            timezone = pytz.timezone("Europe/Berlin")
            current_time = datetime.now(timezone)
            time_str = current_time.strftime("%H:%M")
            date_str = current_time.strftime("%d.%m.%Y")
            return f"Die aktuelle Zeit in Deutschland (Berlin) ist {time_str} Uhr am {date_str}."
        
        # If someone asks about time in general or German time, give them German time
        if any(time_word in city_lower for time_word in time_keywords) or any(germany_word in city_lower for germany_word in germany_keywords):
            timezone = pytz.timezone("Europe/Berlin")
            current_time = datetime.now(timezone)
            time_str = current_time.strftime("%H:%M")
            date_str = current_time.strftime("%d.%m.%Y")
            return f"Die aktuelle Zeit in Deutschland (Berlin) ist {time_str} Uhr am {date_str}."
        
        city_timezones = {
            # International cities
            "germany": "Europe/Berlin",
            "berlin": "Europe/Berlin",
            "münchen": "Europe/Berlin",
            "hamburg": "Europe/Berlin",
            "köln": "Europe/Berlin",
            "frankfurt": "Europe/Berlin",
            "stuttgart": "Europe/Berlin",
            "düsseldorf": "Europe/Berlin",
            "dortmund": "Europe/Berlin",
            "essen": "Europe/Berlin",
            "leipzig": "Europe/Berlin",
            "bremen": "Europe/Berlin",
            "dresden": "Europe/Berlin",
            "hannover": "Europe/Berlin",
            "nürnberg": "Europe/Berlin",
            "duisburg": "Europe/Berlin",
            "bochum": "Europe/Berlin",
            "wuppertal": "Europe/Berlin",
            "bielefeld": "Europe/Berlin",
            "bonn": "Europe/Berlin",
        }
        
        city_key = city.lower()
        if city_key not in city_timezones:
            return f"Entschuldigung, ich kenne die Zeitzone für {city} nicht. Alle deutschen Städte verwenden die gleiche Zeitzone (Europe/Berlin)."
        
        # Special handling for German cities
        if city_key in ["deutschland", "germany", "deutsch", "german", "berlin"]:
            timezone = pytz.timezone("Europe/Berlin")
            current_time = datetime.now(timezone)
            time_str = current_time.strftime("%H:%M")
            date_str = current_time.strftime("%d.%m.%Y")
            return f"Die aktuelle Zeit in Deutschland (Berlin) ist {time_str} Uhr am {date_str}."
        
        timezone = pytz.timezone(city_timezones[city_key])
        current_time = datetime.now(timezone)
        time_str = current_time.strftime("%H:%M")
        date_str = current_time.strftime("%d.%m.%Y")
        return f"Die aktuelle Zeit in {city.title()} ist {time_str} Uhr am {date_str}."
    except Exception as e:
        return f"Fehler: {e}"
