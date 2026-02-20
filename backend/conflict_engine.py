from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Union, Any

# Type hint for daily aggregated data - intermediate stage with lists
DailyRawData = Dict[str, Dict[str, Union[List[float], float]]]

# Final aggregated data type
DailyAggregatedData = Dict[str, Dict[str, float]]

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Union, TypedDict, cast

class DailyRaw(TypedDict):
    temp_list: List[float]
    wind_list: List[float]
    rain: float

# Final aggregated data type
DailyAggregated = Dict[str, Dict[str, float]]

def aggregate_daily(hourly_list: List[dict]) -> DailyAggregated:
    """
    Convert 3-hour forecast list into daily aggregated data.
    Returns: dict[date] -> {"avg_temp": float, "max_wind": float, "rain": float}
    """
    # Use TypedDict for better type checking
    daily: Dict[str, DailyRaw] = {}
    
    for entry in hourly_list:
        dt = datetime.fromtimestamp(entry["dt"])
        date_str = dt.strftime("%Y-%m-%d")
        
        # Initialize if this is the first entry for this date
        if date_str not in daily:
            daily[date_str] = {"temp_list": [], "wind_list": [], "rain": 0.0}
        
        # Now these accesses are type-safe
        daily[date_str]["temp_list"].append(float(entry["main"]["temp"]))
        daily[date_str]["wind_list"].append(float(entry["wind"]["speed"]))
        daily[date_str]["rain"] += float(entry.get("rain", {}).get("3h", 0.0))

    # Aggregate into avg_temp, max_wind, total_rain
    aggregated: DailyAggregated = {}
    for date, vals in daily.items():
        # These are now properly typed as List[float] and float
        temp_list = vals["temp_list"]
        wind_list = vals["wind_list"]
        rain_total = vals["rain"]
        
        avg_temp = sum(temp_list) / len(temp_list) if temp_list else 0.0
        max_wind = max(wind_list) if wind_list else 0.0
        aggregated[date] = {"avg_temp": avg_temp, "max_wind": max_wind, "rain": rain_total}

    return aggregated

def evaluate_day(day_data: Dict[str, float], thresholds: Dict[str, float]) -> Tuple[str, float, float, float]:
    """
    Evaluate a day's weather vs thresholds and return risk.
    """
    avg_temp = day_data.get("avg_temp", 0.0)
    max_wind = day_data.get("max_wind", 0.0)
    rain = day_data.get("rain", 0.0)

    risk = "Green"
    if rain > thresholds.get("max_rain", 0.0) or avg_temp < thresholds.get("min_temp", 0.0) or max_wind > thresholds.get("max_wind", 100.0):
        risk = "Red"
    elif (rain > thresholds.get("max_rain", 0.0) * 0.5 or
          avg_temp < thresholds.get("min_temp", 0.0) * 1.1 or
          max_wind > thresholds.get("max_wind", 100.0) * 0.8):
        risk = "Yellow"

    return risk, avg_temp, max_wind, rain