# #api/main.py — FastAPI REST API để gắn web
# Chạy thử:
# uvicorn api.main:app --reload
# → Truy cập http://127.0.0.1:8000/docs để test API.

from fastapi import FastAPI
from core.solver_route import load_pois, plan_route

app = FastAPI(title="Smart Travel AI")

@app.get("/")
def home():
    return {
        "message": "Smart Travel AI API is running. Visit /docs to test.",
        "docs": "http://127.0.0.1:8000/docs"
    }

@app.post("/plan")
def plan(input_data: dict):
    csv_path = "data/pois_hcm.csv"
    pois = load_pois(csv_path)
    user_prefs = input_data.get("preferences", [])
    start_loc = tuple(input_data.get("start_location", (10.7769, 106.7006)))
    time_window = (input_data["start_time"], input_data["end_time"])
    budget = input_data.get("budget", 1000000.0)

    route = plan_route(pois, user_prefs, start_loc, time_window, budget)

    return {
        "total_stops": len(route),
        "itinerary": [
            {
                "name": r["name"],
                "arrive": r["arrive_time"].strftime("%H:%M"),
                "depart": r["depart_time"].strftime("%H:%M"),
                "mode": r["mode"],
                "cost": int(r["travel_cost"]),
                "entry_fee": int(r["entry_fee"])
            }
            for r in route
        ]
    }
