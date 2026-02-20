from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.weather_service import get_forecast
from backend.threshold_engine import TASK_THRESHOLDS
from backend.schedule_engine import generate_mock_schedule
from backend.conflict_engine import aggregate_daily, evaluate_day
from backend.models import TaskThreshold, WeatherAnalysisResponse
from typing import Dict, List, Any
from datetime import datetime

app = FastAPI(title="SiteBound Weather Scheduler")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/analyze", response_model=Dict[str, WeatherAnalysisResponse])
def analyze(zip: str = Query(..., description="US ZIP code of project site")):
    """
    Analyze weather conditions for scheduled tasks at a given ZIP code.
    Returns a dictionary mapping task names to their weather analysis.
    """
    try:
        # 1️⃣ Fetch forecast
        hourly = get_forecast(zip)

        # 2️⃣ Aggregate daily - returns Dict[str, Dict[str, float]]
        daily = aggregate_daily(hourly)

        # 3️⃣ Mock schedule - assuming this returns Dict[str, str] (task -> date string)
        schedule = generate_mock_schedule()

        # 4️⃣ Evaluate each task
        results: Dict[str, WeatherAnalysisResponse] = {}
        
        for task, date_val in schedule.items():
            # Ensure date is a string
            if isinstance(date_val, datetime):
                date_str = date_val.strftime("%Y-%m-%d")
            elif hasattr(date_val, 'strftime'):  # For date objects
                date_str = date_val.strftime("%Y-%m-%d")
            else:
                date_str = str(date_val)
            
            # Skip if no weather data for this date
            if date_str not in daily:
                print(f"Warning: No weather data for date {date_str}")  # Optional logging
                continue
            
            # Get the day's weather data
            day_data = daily[date_str]
            
            # Get thresholds for this task (this is a Pydantic model)
            task_threshold: TaskThreshold = TASK_THRESHOLDS[task]
            
            # Convert thresholds to dictionary for evaluate_day
            thresholds_dict = {
                "max_rain": 0.0 if task_threshold.allow_rain else 0.1,  # If rain allowed, threshold is 0, else small threshold
                "min_temp": task_threshold.min_temp,
                "max_wind": task_threshold.max_wind
            }
            
            # Evaluate the day
            risk, avg_temp, max_wind, rain = evaluate_day(day_data, thresholds_dict)
            
            # Create response using Pydantic model
            results[task] = WeatherAnalysisResponse(
                task=task,
                date=date_str,
                avg_temp=round(avg_temp, 2),
                max_wind=max_wind,
                rain_detected=rain > 0.01,  # Consider any rain > 0.01mm as rain detected
                risk=risk
            )

        return results

    except KeyError as ke:
        raise HTTPException(status_code=400, detail=f"Task not found: {str(ke)}")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=503, detail="Service unavailable")

# Optional: Add a health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "SiteBound Weather Scheduler"}

# Optional: Add an endpoint to get available tasks
@app.get("/api/tasks", response_model=List[str])
def get_available_tasks():
    """Return list of all available tasks with their thresholds"""
    return list(TASK_THRESHOLDS.keys())