# tools/time_tool.py

from langchain.tools import tool
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

@tool
def get_time(city: str) -> str:
    """Returns the current time in a given city anywhere in the world."""
    try:
        geolocator = Nominatim(user_agent="jarvis-time-tool")
        location = geolocator.geocode(city)

        if not location:
            return f"❌ I couldn't find the location '{city}'. Please try another city."

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)

        if not timezone_str:
            return f"❌ Couldn't determine the timezone for {city}."

        timezone = pytz.timezone(timezone_str)
        current_time = datetime.now(timezone).strftime("%I:%M %p")

        return f"The current time in {city.title()} is {current_time}."

    except Exception as e:
        return f"⚠️ Error while fetching time for {city}: {e}"
