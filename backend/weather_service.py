import requests
from config import API_KEY, BASE_URL, GEO_URL
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_forecast(zip_code: str):
    if not API_KEY:
        raise ValueError("API Key not configured")
    
    geo_response = requests.get(f"{GEO_URL}?zip={zip_code},US&appid={API_KEY}", timeout=10)
    if geo_response.status_code != 200:
        raise ValueError("Invalid Zip Code")
    
    geo = geo_response.json()
    lat, lon = geo["lat"], geo["lon"]

    weather_response = requests.get(f"{BASE_URL}?lat={lat}&lon={lon}&exclude=current,minutely,alerts&units=imperial&appid={API_KEY}", timeout=10)
    if weather_response.status_code == 429:
        raise ValueError("API rate limit exceeded")
    
    data = weather_response.json()
    if "hourly" not in data:
        raise ValueError("Weather data unavailable")
    
    return data["hourly"]