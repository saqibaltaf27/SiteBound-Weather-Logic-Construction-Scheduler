import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"