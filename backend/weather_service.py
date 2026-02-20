import requests
from backend.config import API_KEY, BASE_URL, GEO_URL
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_forecast(zip_code: str):
    if not API_KEY:
        raise ValueError("API Key not configured")
    
    # 1️⃣ Geocode ZIP
    geo_resp = requests.get(GEO_URL, params={"zip": f"{zip_code},US", "appid": API_KEY}, timeout=10)
    if geo_resp.status_code != 200:
        raise ValueError(f"Invalid ZIP or API error: {geo_resp.text}")
    geo = geo_resp.json()
    lat, lon = geo["lat"], geo["lon"]

    # 2️⃣ Get 3-hour forecast
    forecast_resp = requests.get(BASE_URL, params={"lat": lat, "lon": lon, "units": "imperial", "appid": API_KEY}, timeout=10)
    if forecast_resp.status_code == 429:
        raise ValueError("API rate limit exceeded")
    if forecast_resp.status_code != 200:
        raise ValueError(f"Weather API error: {forecast_resp.text}")
    
    data = forecast_resp.json()
    if "list" not in data:
        raise ValueError("Weather data unavailable")

    return data["list"]