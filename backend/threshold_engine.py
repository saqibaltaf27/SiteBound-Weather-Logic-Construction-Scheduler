from backend.models import TaskThreshold

TASK_THRESHOLDS = {
    "Concrete Pouring": TaskThreshold(min_temp=40, max_wind=15, allow_rain=False),
    "Exterior Painting": TaskThreshold(min_temp=50, max_wind=10, allow_rain=False),
    "Roofing": TaskThreshold(min_temp=35, max_wind=20, allow_rain=False),
    "Crane Operations": TaskThreshold(min_temp=30, max_wind=25, allow_rain=False)
}