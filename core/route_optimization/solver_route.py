#core/solver_route.py — Thuật toán chính (Greedy + Lookahead)

# core/algo1/solver_route.py
import pandas as pd
from datetime import datetime, timedelta
from .utils_geo import travel_info
from .scorer import score_candidate
from .config import DEFAULT_BUDGET, DEFAULT_TIME_WINDOW, DEFAULT_START

# ---------- Load POIs ----------
def load_pois(csv_path, filter_tags=None, min_rating=None, max_pois=None):
    """
    Load POIs từ CSV với các filter options
    
    Args:
        csv_path: Đường dẫn đến file CSV
        filter_tags: List các tags cần filter (e.g., ['food', 'park', 'museum'])
        min_rating: Rating tối thiểu (e.g., 4.0)
        max_pois: Giới hạn số lượng POIs (lấy random nếu vượt quá)
    
    Returns:
        List of POI dictionaries
    """
    df = pd.read_csv(csv_path)
    
    # Filter by rating nếu cần
    if min_rating is not None:
        df = df[df["rating"] >= min_rating]
    
    # Filter by tags nếu cần
    if filter_tags:
        # Chọn POIs có ít nhất 1 tag match
        def has_matching_tag(tags_str):
            if not isinstance(tags_str, str):
                return False
            tags = tags_str.split(";")
            return any(tag in filter_tags for tag in tags)
        
        df = df[df["tags"].apply(has_matching_tag)]
    
    # Giới hạn số lượng nếu cần
    if max_pois and len(df) > max_pois:
        df = df.sample(n=max_pois, random_state=42)
    
    # Convert to dict
    pois = df.to_dict("records")
    
    # Remove duplicates based on name (case-insensitive)
    unique_pois = []
    seen_names = set()
    
    for p in pois:
        # Normalize name for duplicate checking
        norm_name = str(p.get("name", "")).lower().strip()
        if norm_name and norm_name not in seen_names:
            p["tags"] = p["tags"].split(";") if isinstance(p["tags"], str) else []
            unique_pois.append(p)
            seen_names.add(norm_name)
    
    return unique_pois

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
            "lat": best_poi["lat"],
            "lon": best_poi["lon"],
            "mode": best_mode,
            "arrive_time": arrive,
            "depart_time": finish,
            "travel_cost": cost,
            "entry_fee": best_poi["entry_fee"],
            "visit_duration_min": best_poi["visit_duration_min"],
            "rating": best_poi.get("rating", 0)
        })

        visited.add(best_poi["id"])
        budget_left -= (best_poi["entry_fee"] + cost)
        current_time = finish
        current_loc = (best_poi["lat"], best_poi["lon"])

    return route
