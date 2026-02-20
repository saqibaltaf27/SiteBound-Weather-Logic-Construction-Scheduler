from pydantic import BaseModel
from typing import Dict

class TaskThreshold(BaseModel):
    min_temp: float
    max_wind: float
    allow_rain: bool

class WeatherAnalysisResponse(BaseModel):
    task: str
    date: str
    avg_temp: float
    max_wind: float
    rain_detected: bool
    risk: str

    