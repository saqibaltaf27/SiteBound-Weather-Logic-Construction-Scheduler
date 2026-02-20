from collections import defaultdict
from datetime import datetime
from models import TaskThreshold

def aggregate_daily(hourly_data):
    daily = defaultdict(list)

    for hour in hourly_data[:168]:
        date = datetime.utcfromtimestamp(hour["dt"]).date()
        daily[date].append(hour)

    return daily


def evaluate_day(hours, threshold: TaskThreshold):
    temps = [h['temp'] for h in hours]
    winds = [h['wind_speed'] for h in hours]
    rain = any('rain' in h for h in hours)
    avg_temp = sum(temps) / len(temps)
    max_wind = max(winds)

    if avg_temp < threshold.min_temp or max_wind > threshold.max_wind:
        return "RED", avg_temp, max_wind, rain
    
    if not threshold.allow_rain and rain:
        return "RED", avg_temp, max_wind, rain
    
    if avg_temp < threshold.min_temp + 5 or max_wind > threshold.max_wind - 5:
        return "YELLOW", avg_temp, max_wind, rain
    
    return "GREEN", avg_temp, max_wind, rain
