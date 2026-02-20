from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from weather_service import get_forecast
from threshold_engine import TASK_THRESHOLDS
from schedule_engine import generate_mock_schedule
from conflict_engine import aggregate_daily, evaluate_day

app = FastAPI(title="Sitebound Weather Scheduler")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/analyze')
def analyze(zip: str):
    try:
        hourly = get_forecast(zip)
        daily = aggregate_daily(hourly)
        schedule = generate_mock_schedule()

        results = {}
        for task, date in schedule.items():
            if date not in daily:
                continue
            risk, avg_temp, max_wind, rain = evaluate_day(daily[date], TASK_THRESHOLDS[task])
            results[task] = {
                "date": str(date),
                "avg_temp": round(avg_temp, 2),
                "max_wind": max_wind,
                "rain_detected": rain,
                "risk": risk,
            }

        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=503, detail="Service unavailable")
    