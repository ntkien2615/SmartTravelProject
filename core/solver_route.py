#core/solver_route.py — Thuật toán chính (Greedy + Lookahead)

# core/solver_route.py
import pandas as pd
from datetime import datetime, timedelta
from core.utils_geo import travel_info
from core.scorer import score_candidate
from core.config import DEFAULT_BUDGET, DEFAULT_TIME_WINDOW, DEFAULT_START

# ---------- Load POIs ----------
def load_pois(csv_path):
    df = pd.read_csv(csv_path)
    pois = df.to_dict("records")
    for p in pois:
        p["tags"] = p["tags"].split(";") if isinstance(p["tags"], str) else []
    return pois

# ---------- Planner ----------
def plan_route(pois, user_prefs=None, start_loc=DEFAULT_START,
               time_window=DEFAULT_TIME_WINDOW, budget=DEFAULT_BUDGET):

    user_prefs = user_prefs or []
    start_time = datetime.strptime(time_window[0], "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(time_window[1], "%Y-%m-%d %H:%M")
    current_time = start_time
    current_loc = start_loc
    budget_left = budget
    route = []
    visited = set()

    while True:
        candidates = []
        for poi in pois:
            if poi["id"] in visited:
                continue
            for mode in ["walking", "motorbike", "taxi"]:
                _, travel_min, cost_vnd = travel_info(current_loc, (poi["lat"], poi["lon"]), mode)
                arrive = current_time + timedelta(minutes=travel_min)
                finish = arrive + timedelta(minutes=poi["visit_duration_min"])

                # Kiểm tra thời gian mở cửa, ngân sách, khung thời gian
                if (arrive.hour < poi["open_hour"] or finish.hour > poi["close_hour"]
                    or budget_left < poi["entry_fee"] + cost_vnd or finish > end_time):
                    continue

                score = score_candidate(poi, travel_min, cost_vnd, user_prefs)
                candidates.append((score, poi, mode, arrive, finish, cost_vnd))

        if not candidates:
            break

        # Chọn POI có score nhỏ nhất (ưu tiên)
        candidates.sort(key=lambda x: x[0])
        best_score, best_poi, best_mode, arrive, finish, cost = candidates[0]

        route.append({
            "id": best_poi["id"],
            "name": best_poi["name"],
            "mode": best_mode,
            "arrive_time": arrive,
            "depart_time": finish,
            "travel_cost": cost,
            "entry_fee": best_poi["entry_fee"]
        })

        visited.add(best_poi["id"])
        budget_left -= (best_poi["entry_fee"] + cost)
        current_time = finish
        current_loc = (best_poi["lat"], best_poi["lon"])

    return route
