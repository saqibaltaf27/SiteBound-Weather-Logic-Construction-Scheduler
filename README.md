# SiteBound: Weather-Logic Construction Scheduler
## Overview

Arbor & Beam Custom Homes specializes in accessory dwelling units (ADUs) and high-end renovations.
This project provides a construction scheduling tool that integrates real-time weather data to identify "No-Go" days for specific weather-sensitive construction activities (e.g., concrete pouring, exterior painting, crane operations).

The system ensures safety and quality by proactively flagging risky days based on thresholds for temperature, wind, and precipitation.

## Features

Threshold Configuration Engine:
Users can define weather-sensitive tasks and set thresholds (e.g., Concrete Pouring: No rain, Temp > 40°F; Roofing: Wind < 20 mph).

Weather API Integration:
Fetches a 7-day hourly forecast from OpenWeatherMap using ZIP codes.

Conflict Detection Logic:
Compares the forecast with a mock project schedule to highlight "Red" (No-Go), "Yellow" (Caution), or "Green" (Go) days.

Project Dashboard:
Displays a clean, web-based weekly view with color-coded risk levels for multiple construction activities.

Error Handling & Resilience:
Gracefully handles invalid ZIP codes, missing data, API rate limits, and network issues.

Folder Structure
SiteBound/
├─ backend/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ config.py
│  ├─ weather_service.py
│  ├─ threshold_engine.py
│  ├─ schedule_engine.py
│  ├─ conflict_engine.py
│  └─ tests/
│     └─ test_conflict_engine.py
├─ frontend/
│  ├─ public/
│  ├─ src/
│  │  ├─ components/
│  │  ├─ pages/
│  │  └─ App.js
│  └─ package.json
├─ requirements.txt
└─ README.md
Installation & Setup
Backend

## Clone the repo:

git clone https://github.com/saqibaltaf27/SiteBound-Weather-Logic-Construction-Scheduler.git
cd SiteBound/backend

Install dependencies:

pip install -r requirements.txt

Set up API Key:
Edit config.py or create a .env file:

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
GEO_URL = "http://api.openweathermap.org/geo/1.0/zip"

Run the backend server:

uvicorn backend.main:app --reload --port 8000

Test API endpoint:
Open Postman or browser:

GET http://127.0.0.1:8000/api/analyze?zip=10001
## Frontend

Navigate to frontend folder:

cd ../frontend

Install Node.js dependencies:

npm install

Run the frontend:

npm start

Open the dashboard in browser at:

http://localhost:3000
Task Configuration

Defined in threshold_engine.py:

TASK_THRESHOLDS = {
    "Concrete Pouring": {"min_temp": 40, "max_wind": 15, "max_rain": 0.0},
    "Roofing": {"min_temp": 32, "max_wind": 20, "max_rain": 0.0},
    "Exterior Painting": {"min_temp": 50, "max_wind": 10, "max_rain": 0.0},
    "Crane Operation": {"min_temp": 32, "max_wind": 25, "max_rain": 0.0},
}

min_temp: Minimum safe temperature (°F)

max_wind: Maximum safe wind speed (mph)

max_rain: Maximum safe rain accumulation (inches)

## How It Works

User inputs ZIP code on frontend.

Backend fetches 7-day hourly forecast from OpenWeatherMap.

aggregate_daily() groups forecast data into daily averages.

evaluate_day() compares daily data against task thresholds.

## Dashboard shows risk levels:

Green: Safe to proceed

Yellow: Exercise caution

Red: No-Go

## Error Handling

Returns 400 Bad Request for invalid ZIP codes or missing API key.

Returns 503 Service Unavailable for API rate limits, network failures, or unavailable weather data.

Frontend displays user-friendly messages for all failures.

## Testing

Backend unit tests are in backend/tests/test_conflict_engine.py.

# Run tests with:

pytest

Ensure backend server is not running when running pytest to avoid port conflicts.

## Deployment

Vercel for frontend

Use environment variables for API key and base URLs in production.

## Demonstration

Fetches weather data for a ZIP code.

Mock schedule is generated for four weather-sensitive tasks.

Dashboard color-codes each task per day based on thresholds.

## Code Quality & Standards

Fully type-hinted Python backend.

Modular functions with clear responsibilities.

Conflict engine logic tested and resilient to missing or malformed data.

Frontend is responsive for both desktop and tablet screens.