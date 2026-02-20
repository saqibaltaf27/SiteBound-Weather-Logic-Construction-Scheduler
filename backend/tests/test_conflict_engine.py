from conflict_engine import evaluate_day
from models import TaskThreshold

def test_red_low_temp():
    hours = [{"temp": 30, "wind_speed": 5}]
    threshold = TaskThreshold(min_temp=40, max_wind=20, allow_rain=False)
    risk, *_ = evaluate_day(hours, threshold)
    assert risk == "RED"

def test_green_conditions():
    hours = [{"temp": 60, "wind_speed": 5}]
    threshold = TaskThreshold(min_temp=40, max_wind=20, allow_rain=False)
    risk, *_ = evaluate_day(hours, threshold)
    assert risk == "GREEN"