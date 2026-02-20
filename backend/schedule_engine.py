from datetime import datetime, timedelta

def generate_mock_schedule():
    today = datetime.utcnow().date()
    return {
        "Concrete Pouring": today + timedelta(days=2),
        "Exterior Painting": today + timedelta(days=3),
        "Roofing": today + timedelta(days=4),
        "Crane Operations": today + timedelta(days=5)
    }